import subprocess as sb
import serial.tools.list_ports
import os
import xml.etree.ElementTree as ET
from time import sleep
from datetime import datetime
from colorama import Fore, Style

def getComPorts():
    ComPort = [port.name for port in serial.tools.list_ports.comports()]
    return ComPort

adb_path = r"adb"

class Devices():

    """Pega as info do dispositivo pela porta e é isso, tem que ter fé"""

    def __init__(self, portaCom):

        self.__portaCom = serial.Serial(portaCom, timeout=3)
        self.getinfo = self.sendAT("AT+DEVCONINFO")
        self.__SN = [port.serial_number for port in serial.tools.list_ports.comports() if port.name == portaCom][0]
        self.__IMEI = self.getinfo[self.getinfo.index("IMEI")+5:self.getinfo.index("IMEI")+20]
        self.__MODEL = self.getinfo[self.getinfo.index("MN")+3:self.getinfo.index("MN")+11]
        self.__CARRIER = self.getinfo[self.getinfo.index("PRD")+4:self.getinfo.index("PRD")+7]
    

        try:
            self.__adbShell("mkdir sdcard/DCIM/AutoScreenshots")
            os.mkdir(rf"{os.getcwd()}\DevicePath\{self.getSN}") 
        except: pass  
    
    def __str__(self):
        return f"{self.getSN},{self.getIMEI},{self.getCARRIER}"


    def sendAT(self, command: str):
        self.__portaCom.write(f"{command}\r\n".encode())
        resposta = self.__portaCom.read(1024)
        return resposta.decode()

    
    @property
    def getSN(self)->str:
        """
        Retorna o Serial Number do Dispositivo
        """
        return self.__SN
    
    @property
    def getPORT(self)->str:
        """
        Retorna a Porta atrelada ao Dispositivo
        """
        return self.__portaCom

    @property
    def getIMEI(self)->str:
        """
        Retorna o IMEI da amostra
        """
        return self.__IMEI
    
    @property
    def getMODEL(self)->str:
        """
        Retorna o Model da amostra
        """
        return self.__MODEL

    @property
    def getCARRIER(self)->str:
        """
        Retorna o Buyer da amostra
        """
        return self.__CARRIER


    def __adbShell(self,command:str) -> str:
        """
        executa um shell command na amostra
        """
        output = sb.run(f"{adb_path} -s {self.__SN} shell {command}",
                            capture_output=True,
                            text=True,
                            shell=True)
        saida = output.stderr

        if output.returncode == 0:
            saida = output.stdout
            
        return saida
    
    def __adbCmd(self,command:str) -> str:
        """
        executa um command CMD na amostra atrelada a Classe
        """
        output = sb.run(f"{adb_path} -s {self.__SN} {command}",
                            capture_output=True,
                            text=True,
                            shell=True)
        saida = output.stderr

        if output.returncode == 0:
            saida = output.stdout
            
        return saida
    
    def click(self, X: float, Y: float) -> str:
        """
        Clica nas coordenadas dadas por X e Y
        """
        output = self.__adbShell(f"input tap {X} {Y}")
        return output
    
    def install(self, pathApp:str)-> str:
        """
        Instala o pacote passado na função
        """
        output = self.__adbCmd(f"install -g {pathApp}")
        return output.splitlines()

    def openActivity(self, activity:str)-> str:
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
    
    def keyEvent(self, number:int) ->None:
        self.__adbShell(f"input keyevent {number}")

    def makeCall(self, number:str)-> str:
        self.keyEvent("KEYCODE_CALL")
        self.input_text(number)
        self.keyEvent(5)
        sleep(2)
        self.screenshot(f"Call_{number}")
        self.keyEvent(5)
        self.keyEvent(3)

    def screenshot(self, local:str)-> str:
        hoje = datetime.now()
        output = self.__adbShell(f"screencap -p /sdcard/DCIM/AutoScreenshots/{hoje.day}_{hoje.hour}_{hoje.minute}_{hoje.microsecond}_{local}.png")
        print(f"{self.getSN}: print de {local}")
            
        return output
    
    def input_text(self, text:str):
        self.__adbShell(f"input text {text}")

    def swipeDown(self):
        self.__adbShell("input swipe 300 1000 500 300")

    def swipeUp(self):
        self.__adbShell("input swipe 300 300 500 1000")

    def getWindowDump(self) -> str:
        output = self.__adbCmd('exec-out uiautomator dump /dev/tty').replace("UI hierchary dumped to: /dev/tty",'')
        return output
    
    def findButtonID(self, ID:str) -> list:
        """Procura um botão ou 'Div' na tela pelo ID e clica em seguida"""
        root = ET.fromstring(self.getWindowDump())

        for tag in root.iter('node'):
            if tag.attrib['resource-id'] == ID:
                result = tag.attrib["bounds"]
                result = result.replace("][", ",")
                result = ((result[1:-1]).split(","))
                break
           
        
        coodenadas_finais = {
            "A1": int(result[0]),
            "B1": int(result[1]),
            "A2": int(result[2]),
            "B2": int(result[3])
        }

        x = (coodenadas_finais["A2"] - coodenadas_finais["A1"])/2 + coodenadas_finais["A1"]
        y = (coodenadas_finais["B2"] - coodenadas_finais["B1"])/2 + coodenadas_finais["B1"]

        self.click(x,y)
        return [x,y]
    
    def findButtonTEXT(self, Text:str) -> tuple[float, float]:
        """Procura um botão ou 'Div' na tela pelo texto e clica em seguida"""
        root = ET.fromstring(self.getWindowDump())

        for tag in root.iter('node'):
            if tag.attrib['text'] == Text:
                result = tag.attrib["bounds"]
                result = result.replace("][", ",")
                result = ((result[1:-1]).split(","))
                break
        
        coodenadas_finais = {
            "A1": int(result[0]),
            "B1": int(result[1]),
            "A2": int(result[2]),
            "B2": int(result[3])
        }
        x = (coodenadas_finais["A2"] - coodenadas_finais["A1"])/2 + coodenadas_finais["A1"]
        y = (coodenadas_finais["B2"] - coodenadas_finais["B1"])/2 + coodenadas_finais["B1"]

        self.click(x,y)
        return x,y
    
    def listAllButtons(self) -> list:
        root = ET.fromstring(self.getWindowDump())
        buttons = []

        for tag in root.iter('node'):
            if tag.attrib["clickable"] == "true":
                buttons.append([tag.attrib['resource-id'],
                                tag.attrib['text'],
                            tag.attrib['bounds']])

        return buttons
    
    def clickInWithBounds(self, bounds:str = None):
        bounds = bounds.replace("][", ",")[1:-1].split(",")
        x = (int(bounds[2]) - int(bounds[0]))/2 + int(bounds[0])
        y = (int(bounds[3]) - int(bounds[1]))/2 + int(bounds[1])
            
        self.click(x,y)

    def apnTest(self):
        self.openActivity("android.settings.WIRELESS_SETTINGS")
        sleep(0.5)
        self.screenshot("WIRELESS_SETTINGS")
        
        self.openActivity("android.settings.DATA_ROAMING_SETTINGS")
        sleep(0.5)
        self.screenshot("DATA_ROAMING_SETTINGS")
        
        lin = self.__adbShell("getprop mdc.sys.locale")
        
        if "pt-BR" in lin:
            self.findButtonTEXT("Pontos de acesso")
        else:
            self.findButtonTEXT("Nombres de punto de acceso")    
        sleep(0.5)

        self.screenshot("APN_SETTINGS")
        self.keyEvent("KEYCODE_APP_SWITCH")
        try: self.findButtonID("com.sec.android.app.launcher:id/clear_all_button")    
        except: self.findButtonID("com.sec.android.app.launcher:id/clear_all")
        
        print(self.getSN,Fore.GREEN +"APN PASS"+Style.RESET_ALL)

    ########################## Rotinas ###########################

    def getMCCMNCfromCostumer(self):
        local = self.__adbShell("getprop persist.sys.omc_path")
        print(f"Local do Arquivo identificado: {local.strip()}")
        customer = self.__adbShell("cat {}/customer.xml".format(local.strip()))

        root = ET.fromstring(customer)
        networks = []

        for tag in root.iter("MCCMNC"):
            networks.append(tag.text)

        networks = list(set(networks))
        print(f"{self.getSN}:",f"Redes encontradas: {networks}")
        
        return networks
    

    

       
    def googleClientID(self):
        pacotes = self.__adbShell("pm list packages -3")
        print('listou os pacotes')
       

        if "package:com.sec.keystringmain" in pacotes:
            pass
        else:
            saida = self.install("apps\Keystring_v3.9_Official.apk")
            print(saida)
            if "Success" not in saida:
                self.install("apps\Keystring_v3.9_RIZE_Official.apk")

        self.openApp("com.sec.keystringmain/com.sec.keystringmain.MainActivity")
        windowDump = self.getWindowDump()
        root = ET.fromstring(windowDump)
        for tag in root.iter('node'):
            if tag.attrib['resource-id'] == "com.sec.keystringmain:id/buttonSendKeystring":
                botao = tag.attrib["bounds"]
                break
        
        self.input_text("*#6628378#")
        self.clickInWithBounds(botao)
        self.findButtonID("com.samsung.android.app.omcagent:id/sesl_action_bar_overflow_button")
        self.findButtonTEXT("Input Command")
        self.input_text("adcp")
        self.findButtonID("android:id/button1")
        self.swipeDown()
        self.screenshot("Google_Client_ID")
