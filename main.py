import tkinter as tk					 
from tkinter import ttk 
from Device import Devices, getComPorts
import threading


root = tk.Tk() 
root.title("Tab Widget") 
tabControl = ttk.Notebook(root) 

ports = getComPorts()
deviceObjs:[Devices] = []

def creatorDevices(pt):
    d = Devices(pt)
    deviceObjs.append(d)


thList = [threading.Thread(target=creatorDevices,args=(port,)) for port in ports]    

[i.start() for i in thList]
[i.join() for i in thList]

root.geometry(f"{500}x{200}")

for obj in deviceObjs:
    tab1 = ttk.Frame(tabControl) 

    tabControl.add(tab1, text =f"{obj.getMODEL} / {obj.getCARRIER}") 
    tabControl.pack(expand = 1, fill ="both") 

    ttk.Label(tab1, text =f"Device: {obj.getSN}").grid(column = 0, row = 0, padx = 5, pady = 5) 
    ttk.Label(tab1, text =f"Imei: {obj.getIMEI}").grid(column = 0, row = 1, padx = 5, pady = 5) 
    ttk.Label(tab1, text =f"Carrier: {obj.getCARRIER}").grid(column = 0, row = 2, padx = 5, pady = 5) 
    ttk.Label(tab1, text =f"Carrier: {obj.getMODEL}").grid(column = 0, row = 3, padx = 5, pady = 5) 
root.mainloop() 
