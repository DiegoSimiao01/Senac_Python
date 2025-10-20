
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from cadastro import abrir_cadastro

AZUL = "#0a2c61"
LARANJA = "#e68a00"
BRANCO = "#ffffff"

def placeholder(entry, text):
    """Adiciona um texto temporário (placeholder) a um campo de entrada."""
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


def abrir_login():
    """Cria e exibe a janela de login."""
    window_login = tk.Tk()
    window_login.title("Login")
    window_login.geometry("900x600")

    def ir_para_cadastro():
        """Fecha a janela de login e abre a de cadastro."""
        window_login.destroy()
        abrir_cadastro(abrir_login)

    # --- FRAME ESQUERDA (LOGO) ---
    frame_esquerda = tk.Frame(window_login, bg=AZUL, width=280, height=550)
    frame_esquerda.pack(side="left", fill="y")

    try:
        img = Image.open("senacbranco.png")
        img = img.resize((175, 150))
        logo = ImageTk.PhotoImage(img)
        lbl_logo = tk.Label(frame_esquerda, image=logo, bg=AZUL)
        lbl_logo.image = logo 
        lbl_logo.place(x=50, y=190)
    except FileNotFoundError:
        print("Arquivo 'senacbranco.png' não encontrado. Verifique o caminho.")

    # --- FRAME DIREITA LOGIN ---
    frame_direita = tk.Frame(window_login, bg=BRANCO)
    frame_direita.pack(side="right", expand=True, fill="both")

    lbl_title = tk.Label(frame_direita, text="Login Senac", font=("Arial", 18, "bold"), bg=BRANCO, fg="gray")
    lbl_title.place(x=250, y=80)
    lbl_sub = tk.Label(frame_direita, text="Bem-vindo ao Sistema de Controle de Empréstimo de Drone", font=("Arial", 10), bg=BRANCO, fg="gray")
    lbl_sub.place(x=130, y=120)

    # Entradas
    lbl_user = tk.Label(frame_direita, text="Login *", fg="gray", font=("Arial", 10), bg=BRANCO)
    lbl_user.place(x=200, y=185)
    entry_user = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3)
    entry_user.place(x=200, y=210, height=30)
    placeholder(entry_user, "Username")

    lbl_senha = tk.Label(frame_direita, text="Senha *", fg="gray", font=("Arial", 10), bg=BRANCO)
    lbl_senha.place(x=200, y=255)
    entry_senha = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3, show="*")
    entry_senha.place(x=200, y=280, height=30)
    placeholder(entry_senha, "**********")

    # --- BOTÕES ---
    btn_login = tk.Button(frame_direita, text="Login", bg=AZUL, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3)
    btn_login.place(x=200, y=350, height=30)
    
   
    btn_cadastro = tk.Button(frame_direita, text="Cadastrar-se", bg=LARANJA, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3, command=ir_para_cadastro)
    btn_cadastro.place(x=200, y=390, height=30)
    
    window_login.mainloop()
