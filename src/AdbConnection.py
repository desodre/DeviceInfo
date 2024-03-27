from datetime import datetime
from time import sleep
from serial import Serial
import serial.tools.list_ports
import os
import subprocess


class SerialConnect(Serial):
    """Pega as info do dispositivo pela porta e é isso, tem que ter fé"""

    def __init__(
        self,
        port: str | None = None,
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: float = 1,
        timeout: float | None = None,
        xonxoff: bool = False,
        rtscts: bool = False,
        write_timeout: float | None = None,
        dsrdtr: bool = False,
        inter_byte_timeout: float | None = None,
        exclusive: float | None = None,
    ) -> None:
        super().__init__(
            port,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=None,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )

        self.DeviceInfos = self.SendAT("AT+DEVCONINFO")
        self.__IMEI = self.DeviceInfos[
            self.DeviceInfos.index("IMEI") + 5 : self.DeviceInfos.index("IMEI") + 20
        ]
        self.__MODEL = self.DeviceInfos[
            self.DeviceInfos.index("MN") + 3 : self.DeviceInfos.index("MN") + 11
        ]
        self.__CARRIER = self.DeviceInfos[
            self.DeviceInfos.index("PRD") + 4 : self.DeviceInfos.index("PRD") + 7
        ]
        self.__SERIALNUMBER = self.DeviceInfos[
            self.DeviceInfos.index("SN") + 3 : self.DeviceInfos.index("SN") + 14
        ]

    def __str__(self) -> str:
        return f"{self.__SERIALNUMBER},{self.__IMEI},{self.__CARRIER}"  

    def SendAT(self, command: str | bytes):
        """Envia e lê comandos AT no dispositivo"""
        self.write(command.encode())
        saida: bytes = self.read(400)
        return saida.decode()

    def retornatudo(self):
        return {"IMEI": self.__IMEI, "MODEL": self.__MODEL, "CARRIER": self.__CARRIER}

    @property
    def getSN(self):
        return self.__SERIALNUMBER


class AdbConnect:
    def __init__(self, serialCode) -> None:
        self.serialCode = serialCode
        self.__adbPath = os.path.join(
            os.getcwd(), r"Adb\adb.exe"
        )  # usei o join para mesclar os dois caminhos sem erro de parse ou erro de variavel de ambiente

    def __adbCmd(self, command: str) -> str:
        retorno = subprocess.run(
            f"{self.__adbPath} -s {self.serialCode} {command}",
            text=True,
            capture_output=True,
        )

        return retorno

    def __adbShell(self, command: str) -> str:
        retorno = subprocess.run(
            f"{self.__adbPath} -s {self.serialCode} shell {command}",
            text=True,
            capture_output=True,
        )
 
        return retorno

    def click(self, X: float, Y: float) -> str:
        """
        Clica nas coordenadas dadas por X e Y
        """
        output = self.__adbShell(f"input tap {X} {Y}")
        return output

    def install(self, pathApp: str) -> str:
        """
        Instala o pacote passado na função
        """
        output = self.__adbCmd(f"install -g {pathApp}")
        return output.splitlines()

    def openActivity(self, activity: str) -> str:
        """
        Abre uma Activity no dispositivo
        """
        output = self.__adbShell(f"am start -a {activity}")
        return output

    def openApp(self, appPath: str) -> str:
        """
        Abre uma Main Activity no dispositivo
        """
        output = self.__adbShell(f"am start {appPath}")
        return output

    def keyEvent(self, number: int) -> None:
        self.__adbShell(f"input keyevent {number}")

    def makeCall(self, number: str) -> str:
        self.keyEvent("KEYCODE_CALL")
        self.input_text(number)
        self.keyEvent(5)
        sleep(2)
        self.screenshot(f"Call_{number}")
        self.keyEvent(5)
        self.keyEvent(3)

    def screenshot(self, local: str) -> str:
        hoje = datetime.now()
        output = self.__adbShell(
            f"screencap -p /sdcard/DCIM/AutoScreenshots/{hoje.day}_{hoje.hour}_{hoje.minute}_{hoje.microsecond}_{local}.png"
        )
        print(f"{self.serialCode}: print de {local}")

        return output

    def input_text(self, text: str):
        self.__adbShell(f"input text {text}")

    def swipeDown(self):
        self.__adbShell("input swipe 300 1000 500 300")

    def swipeUp(self):
        self.__adbShell("input swipe 300 300 500 1000")

    def getWindowDump(self) -> str:
        output = self.__adbCmd("exec-out uiautomator dump /dev/tty")
        return output


def get_all_ports() -> list[str]:
    return [
        port.name
        for port in serial.tools.list_ports.comports()
        if "Bluetooth" not in port.description
    ]


if __name__ == "__main__":
    ComPort = get_all_ports()
    con = SerialConnect(ComPort[0])
    device = AdbConnect(con.getSN)
    print(device.getWindowDump())
