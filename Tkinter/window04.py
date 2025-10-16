import tkinter as tk
from tkinter import messagebox as msg

window = tk.Tk()
window.geometry("350x200")
window.title('Organizador de Arquivos')

label = tk.Label(window, text="Pasta Selecionada")
label.pack(pady=10)

entry = tk.Entry(window, width=30)
entry.pack(pady=5)

botao_selecionar = tk.Button(window, text="Selecionar Pasta")
botao_selecionar.pack(pady=10)

botao_organizar = tk.Button(window, text="Organizar Arquivos")
botao_organizar.pack(pady=10)

window.mainloop()