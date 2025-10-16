import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Configurações iniciais
ctk.set_appearance_mode("dark") # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue") # Themes: blue (default), dark-blue, green

# Janela principal
window = ctk.CTk() # Create CTk window like you do with the Tk window
window.geometry("700x500")
window.title("Projeto")  

# Frames
frame_cadastro = ctk.CTkFrame(window)
frame_cadastro.place(x=20, y=20)

frame_imagem = ctk.CTkFrame(window, width=200, height=200)
frame_imagem.place(x=400, y=20)

# Upload e exibição de imagem
img = Image.open('pasta.png')
img = img.resize((100, 80),Image.Resampling.NEAREST)
img_tk = ImageTk.PhotoImage(img)

label_img = ctk.CTkLabel(frame_imagem, image=img_tk, text="")
label_img.place(x=50, y=50)


btn_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar")
btn_cadastrar.place(y=12, x=10)

window.mainloop()
