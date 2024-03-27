from src.AdbConnection import SerialConnect, get_all_ports


ComPort = get_all_ports()

if len(ComPort) == 0:
    print("Nenhuym disposivo detectado . . .")
else:
    for port in ComPort:
        device = SerialConnect(port)
        print(device)
    
input("Clique qualquer tecla para finalizar ...")
