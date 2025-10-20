# Arquivo: cadastro.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Cores ---
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

def abrir_cadastro(on_close_callback):
    """
    Cria e exibe a janela de cadastro.
    on_close_callback: A função que deve ser chamada ao fechar esta janela.
    """
    window_cadastro = tk.Tk()
    window_cadastro.title("Cadastro")
    window_cadastro.geometry("900x600")

    def voltar_para_login():
        """Fecha a janela de cadastro e executa a função de callback."""
        window_cadastro.destroy()
        on_close_callback()

    # --- FRAME ESQUERDA (LOGO) ---
    frame_esquerda = tk.Frame(window_cadastro, bg=AZUL, width=280, height=550)
    frame_esquerda.pack(side="left", fill="y")
    
    try:
        img = Image.open("senacbranco.png")
        img = img.resize((175, 150))
        logo = ImageTk.PhotoImage(img)
        lbl_logo = tk.Label(frame_esquerda, image=logo, bg=AZUL)
        lbl_logo.image = logo
        lbl_logo.place(x=50, y=190)
    except FileNotFoundError:
        print("Arquivo 'senacbranco.png' não encontrado.")

    # --- FRAME DIREITA CADASTRO ---
    frame_direita = tk.Frame(window_cadastro, bg=BRANCO)
    frame_direita.pack(side="right", expand=True, fill="both")

    lbl_title = tk.Label(frame_direita, text="Cadastrar-se no Sistema", font=("Arial", 18, "bold"), bg=BRANCO, fg="gray")
    lbl_title.place(x=180, y=80)

    lbl_sub = tk.Label(frame_direita, text="Bem-vindo ao Sistema de Controle de Empréstimo de Drone", font=("Arial", 10), bg=BRANCO, fg="gray")
    lbl_sub.place(x=140, y=120)

    # Entradas de cadastro
    lbl_user = tk.Label(frame_direita, text="Usuario", fg="gray", font=("Arial", 10), bg=BRANCO)
    lbl_user.place(x=200, y=185)
    entry_user = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3)
    entry_user.place(x=200, y=210, height=30)
    placeholder(entry_user, "Username")

    lbl_codigo = tk.Label(frame_direita, text="Código de Funcionário", fg="gray", font=("Arial", 10), bg=BRANCO)
    lbl_codigo.place(x=200, y=255)
    entry_codigo = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3)
    entry_codigo.place(x=200, y=280, height=30)
    placeholder(entry_codigo, "Digite seu código")

    lbl_senha = tk.Label(frame_direita, text="Senha", fg="gray", font=("Arial", 10), bg=BRANCO)
    lbl_senha.place(x=200, y=320)
    entry_senha = tk.Entry(frame_direita, font=("Arial", 10), width=35, relief="flat", bd=3, show="*")
    entry_senha.place(x=200, y=345, height=30)
    placeholder(entry_senha, "Crie uma senha")

    # Botões
    btn_cadastrar = tk.Button(frame_direita, text="Cadastrar-se", bg=AZUL, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3)
    btn_cadastrar.place(x=200, y=420, height=30)

    btn_voltar = tk.Button(frame_direita, text="Voltar ao Login", bg=LARANJA, fg=BRANCO, font=("Arial", 10), width=32, relief="flat", bd=3, command=voltar_para_login)
    btn_voltar.place(x=200, y=460, height=30)
    
    window_cadastro.mainloop()