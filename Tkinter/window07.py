import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.geometry('500x600')
janela.grid_columnconfigure(0, weight=1)

frame_cadastro = tk.LabelFrame(text='Cadastro')
frame_cadastro.grid(sticky="nsew",padx=10,pady=10)

label_nome = tk.Label(frame_cadastro,text='Nome:',width=10)
label_nome.grid(row=0, column=0,padx=5,pady=5)

entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1,padx=5,pady=5)

frame02 = tk.LabelFrame(text='Registro')
frame02.grid(sticky="nsew",padx=10,pady=10)

label01 = tk.Label(frame02,text='Idade:',width=10)
label01.grid(row=0, column=0,padx=5,pady=5)

entry01 = tk.Entry(frame02)
entry01.grid(row=0, column=1,padx=5,pady=5)

frame_tabela = tk.LabelFrame(text='Registros')
frame_tabela.grid(sticky="nsew",padx=10,pady=10)
frame_tabela.grid_columnconfigure(0, weight=1)

tabela = ttk.Treeview(frame_tabela,columns=('Nome','Idade'),show='headings') #Treeview = tabela
tabela.grid(row=0,column=0,sticky="nsew")
tabela.heading('Nome',text='Nome') # Define o cabeçalho da coluna
tabela.heading('Idade',text='Idade')
tabela.column('Nome',width=300)
tabela.column('Idade',width=150)

def adicionar():
    nome = entry_nome.get()
    idade = entry01.get()
    tabela.insert('', 'end', values=(nome, idade))
    entry_nome.delete(0, tk.END)
    entry01.delete(0, tk.END)

botao_adicionar = tk.Button(frame02,text='Adicionar',command=adicionar)
botao_adicionar.grid(row=1,column=0,columnspan=2,pady=10,padx=5, sticky="nsew")

janela.mainloop()