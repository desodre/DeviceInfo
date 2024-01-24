from Device import Devices, getComPorts
import threading


def main(porta):
    dispositivo = Devices(portaCom=porta)
    print(f"{dispositivo.getSN},{dispositivo.getIMEI},{dispositivo.getCARRIER}")
    #dispositivo.googleClientID()
    dispositivo.apnTest()
    input("Enter to close")


ComPort = getComPorts()

if __name__ == '__main__':
    for porta in ComPort:
        deviceProcess = threading.Thread(target=main, args=(porta,))
        deviceProcess.start()