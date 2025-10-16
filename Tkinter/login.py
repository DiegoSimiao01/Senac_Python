import tkinter as tk
from tkinter import messagebox as msg

dados = {'admin': '123456'}

def abrir_cadastro():

    def fazer_cadastro():
        usuario = entry_cad_usuario.get()
        senha = entry_cad_senha.get()
        if usuario in dados:
            msg.showerror("Erro", "Usuário já cadastrado!")
        elif usuario == '' or senha == '':
            msg.showerror("Erro", "Preencha usuário e senha!")
        else:
            dados[usuario] = senha
            msg.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            window_cadastrar.destroy()
            abrir_login()

    window_cadastrar = tk.Tk()
    window_cadastrar.title('Cadastro') 
    window_cadastrar.geometry("300x400") 

    label_cadastro = tk.Label(window_cadastrar, text="Cadastro de usuário", font=('Arial',14)) 
    label_cadastro.pack(pady=5) 

    label_cad_usuario = tk.Label(window_cadastrar, text='Usuário') 
    label_cad_usuario.pack(pady=5) 
    label_cad_usuario.pack(padx=(0,80))

    entry_cad_usuario = tk.Entry(window_cadastrar)
    entry_cad_usuario.pack(pady=5) 

    label_cad_senha = tk.Label(window_cadastrar, text='Senha')
    label_cad_senha.pack(pady=5) 
    label_cad_senha.pack(padx=(0,90))

    entry_cad_senha = tk.Entry(window_cadastrar) 
    entry_cad_senha.pack(pady=5) 

    botao_cadastro = tk.Button(window_cadastrar, text="Cadastrar", command=fazer_cadastro) 
    botao_cadastro.pack(pady=(15,0))
    botao_cadastro.pack(padx=(0,60))

    def voltar_login():
            window_cadastrar.destroy()
            abrir_login()

    botao_voltar = tk.Button(window_cadastrar, text="Voltar", command=voltar_login)
    botao_voltar.pack(pady=(15,0))
    botao_voltar.pack(padx=(0,80))

    label_result = tk.Label(window_cadastrar, text="")
    label_result.pack(pady=(20,0))

def abrir_login():
    
    def fazer_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if usuario in dados and dados[usuario] == senha:
            label_resultado.config(text='Login efetuado com sucesso!')
        else:
            label_resultado.config(text='Usuario ou senha incorretos!')

    window = tk.Tk()
    window.title('Login') 
    window.geometry("300x400") 

    label = tk.Label(window, text="Acesso ao Sistema", font=('Arial',14)) 
    label.pack(pady=5) 

    label_usuario = tk.Label(window, text='Usuário') 
    label_usuario.pack(pady=5) 
    label_usuario.pack(padx=(0,80))

    entry_usuario = tk.Entry(window)
    entry_usuario.pack(pady=5) 

    label_senha = tk.Label(window, text='Senha')
    label_senha.pack(pady=5) 
    label_senha.pack(padx=(0,90))

    entry_senha = tk.Entry(window,show='*') 
    entry_senha.pack(pady=5) 

    botao_login = tk.Button(window, text="Login", command=fazer_login) 
    botao_login.pack(pady=(30,0))
    botao_login.pack(padx=(0,80))

    def abrir_e_fechar_cadastro():
        window.destroy()
        abrir_cadastro()

    botao_cadastrar = tk.Button(window, text="Cadastrar", command=abrir_e_fechar_cadastro)
    botao_cadastrar.pack(pady=(15,0))
    botao_cadastrar.pack(padx=(0,60))

    label_resultado = tk.Label(window, text="")
    label_resultado.pack(pady=(20,0))

    window.mainloop() 

abrir_login()
