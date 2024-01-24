import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk

#Janela principal
window = ttk.Window(themename="journal")
window.title("Demonstração")
window.geometry("400x150")

def converter():
    print(EntradaInt.get() * 1.60934)
    output_String.set(f"{EntradaInt.get() * 1.60934}")


#Titulo
title_Lable = ttk.Label(master= window, text="Milhas para quilometros", font="Times 20")
title_Lable.pack()

#Campo de entrada
input_Frame = ttk.Frame(master=window)
EntradaInt = tk.IntVar()
entrada = ttk.Entry(master=input_Frame, textvariable=EntradaInt)
botao = ttk.Button(master=input_Frame, text="Converter", command=converter)
entrada.pack(side="left", padx=20)
botao.pack(side="left")
input_Frame.pack(pady=10)

#campo de saida
output_String = tk.StringVar()
output_Lable = ttk.Label(master=window,
                          text="Saideira",
                            font="Times 15 bold",
                              textvariable=output_String)
output_Lable.pack(pady=10)



window.mainloop()