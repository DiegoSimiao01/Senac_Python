import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

### Cores
AZUL = "#0a2c61"
LARANJA = "#e68a00"
BRANCO = "#ffffff"

### Janela principal
window_login = tk.Tk()
window_login.title("Cadastro")
window_login.geometry("900x600")

###FRAME ESQUERDA (LOGO)
frame_esquerda = tk.Frame(window_login, bg=AZUL, width=280, height=550)
frame_esquerda.pack(side="left", fill="y")

###Carregar imagem do logo 
img = Image.open("senacbranco.png")  # coloquar sempre no mesmo diretório
img = img.resize((175, 150))
logo = ImageTk.PhotoImage(img)
lbl_logo = tk.Label(frame_esquerda, image=logo, bg=AZUL)
lbl_logo.place(x=50, y=190)

###FRAME DIREITA CADASTRO
frame_direita = tk.Frame(window_login, bg=BRANCO)
frame_direita.pack(side="right", expand=True, fill="both")

### Título
lbl_title = tk.Label(frame_direita, text="Cadastrar-se no Sistema", font=("Arial", 18, "bold"), bg=BRANCO)
lbl_title.place(x=180, y=80)

lbl_sub = tk.Label(frame_direita, text="Bem-vindo ao Sistema de Controle de Empréstimo de Drone",font=("Arial", 10), bg=BRANCO, fg="gray")
lbl_sub.place(x=140, y=120)

def placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == text:
           entry.delete(0, "end")
           entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
           entry.insert(0, text)
           entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
### Entradas
lbl_user = tk.Label(frame_direita, text="Usuario", fg="gray",font=("Arial", 10), bg=BRANCO)
lbl_user.place(x=200, y=185)
entry_user = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3)
entry_user.place(x=200, y=210, height=30)
placeholder(entry_user, "Username")

lbl_cadastro = tk.Label(frame_direita, text="Código de Funcionário", fg="gray", font=("Arial", 10), bg=BRANCO)
lbl_cadastro.place(x=200, y=255)
entry_cadastro = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3, show="")
entry_cadastro.place(x=200, y=280, height=30)
placeholder(entry_cadastro, "Digite seu código")

lbl_senha = tk.Label(frame_direita, text="Senha", fg="gray", font=("Arial", 10), bg=BRANCO)
lbl_senha.place(x=200, y=320)
entry_senha = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3, show="")
entry_senha.place(x=200, y=345, height=30)
placeholder(entry_senha, "Crie uma senha")

###BOTÕES
btn_login = tk.Button(frame_direita, text="Cadastrar-se", bg=AZUL, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3)
btn_login.place(x=200, y=420, height=30)

btn_cadastro = tk.Button(frame_direita, text="Voltar ao Login", bg=LARANJA, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3)
btn_cadastro.place(x=200, y=460, height=30)

window_login.mainloop()
