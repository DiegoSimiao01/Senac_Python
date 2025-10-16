import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry("800x600")
window.title('Cadastro de Clientes')

frame1 = tk.LabelFrame(text='Dados',bg='lightgray')
frame1.grid(sticky="nsew")
window.grid_columnconfigure(0, weight=1)

label_nome = tk.Label(frame1, text="Nome:",bg='lightgray')
label_nome.grid(row=0, column=0, padx=0, pady=5,sticky="w")

entry_nome = tk.Entry(frame1, width=20)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

botao_pesquisar = tk.Button(frame1, width=15, text="Pesquisar", bg='blue', fg='white')
botao_pesquisar.grid(row=0, column=3, padx=5, pady=5)

entry_pesquisar = tk.Entry(frame1, width=20)
entry_pesquisar.grid(row=0, column=4, padx=5, pady=5)

label_email = tk.Label(frame1, text="Email:",bg='lightgray')
label_email.grid(row=1, column=0, padx=0, pady=5,sticky="w")

entry_email = tk.Entry(frame1, width=20)
entry_email.grid(row=1, column=1, padx=5, pady=5)

label_telefone = tk.Label(frame1, text="Telefone:",bg='lightgray')
label_telefone.grid(row=2, column=0, padx=0, pady=5,sticky="w")

entry_telefone = tk.Entry(frame1, width=20)
entry_telefone.grid(row=2, column=1, padx=5, pady=5)

def adicionar():

    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    if nome == '' or email == '' or telefone == '':
        return
    tabela.insert('', 'end', values=('',nome, email, telefone))
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

botao_cadastro = tk.Button(frame1, text="Cadastrar(Enter)",command=adicionar, bg='blue', fg='white')
botao_cadastro.grid(row=3, column=0, padx=0, pady=10,sticky="w")

botao_limpar = tk.Button(frame1, width=15, text="Limpar(F2)", bg='blue', fg='white')
botao_limpar.grid(row=3, column=1, padx=5, pady=10)

botao_excluir = tk.Button(frame1,width=15, text="Excluir(Delete)", bg='blue', fg='white')
botao_excluir.grid(row=3, column=2, padx=5, pady=10)

botao_apagar = tk.Button(frame1,width=15, text="Desfazer(Apagar)", bg='blue', fg='white')
botao_apagar.grid(row=3, column=3, padx=5, pady=10)

botao_salvar = tk.Button(frame1, width=15, text="Salvar", bg='blue', fg='white')
botao_salvar.grid(row=3, column=4, padx=5, pady=10)

frame_tabela = tk.LabelFrame(text='Clientes Cadastrados', bg='lightgray')
frame_tabela.grid(sticky="nsew",padx=10,pady=10)
frame_tabela.grid_columnconfigure(0, weight=1)

botao_remover = tk.Button(frame_tabela, width=18, text="Remover Selecionados", bg='blue', fg='white')
botao_remover.grid(row=0,column=0, padx=5, pady=5, sticky="en")

tabela = ttk.Treeview(frame_tabela,columns=('Id','Nome', 'email', 'telefone'),show='headings') #Treeview = tabela
tabela.grid(row=1,column=0,sticky="nsew")
tabela.heading('Id',text='Id') # Define o cabeçalho da coluna
tabela.heading('Nome',text='Nome')
tabela.heading('email',text='email')
tabela.heading('telefone',text='telefone')
tabela.column('Id',width=50)
tabela.column('Nome',width=200)
tabela.column('email',width=200)
tabela.column('telefone',width=150)





window.mainloop()