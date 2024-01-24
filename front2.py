import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from Device import getComPorts, Devices


serialPorts = getComPorts()


class MyApp(ttk.Window):
    def __init__(self):
        super().__init__()
    

        self.title("Serial Reader")
        self.geometry("600x300")

        frame1 = ttk.Label(master=self,background="Blue", text="Vermelho")
        frame1.pack(side="left", fill="both", expand=True)

        frame1Sub1 = ttk.Label(master=frame1)
        frame1Sub1.pack(side="top",fill="x")

        self.selectPort = ttk.Combobox(master=frame1Sub1, values=serialPorts)
        self.selectPort.pack(side="left", padx=5)


        ExectuteCommandButton = ttk.Button(master=frame1Sub1, text="Send Command", command=self.ExecCommand)#ainda nao tem comando pra executar
        ExectuteCommandButton.pack(side="right", padx=5)

        self.outputString = tk.StringVar()
        frame2 = ttk.Label(master=self,background="red", width=50, text="Azul", textvariable=self.outputString)
        frame2.pack(side="right", fill="both", expand=True)

        #Run all
        self.mainloop()

    def outPort(self):
        saida = self.selectPort.get()
        print(saida)

    def ExecCommand(self):
        dispositivo = Devices(portaCom = self.selectPort.get())
        saidaAT = dispositivo.sendAT("AT+DEVCONINFO")
        saidaList = [print(bloco) for bloco in saidaAT.split(";")]
        self.outputString.set(" ".join(saidaList))

    


MyApp()