import tkinter as tk

window = tk.Tk()
window.geometry("380x300")
window.title('Aula de frames')

frame1 = tk.LabelFrame(text='Cadastro')
frame1.grid(pady=10)

label_nome = tk.Label(frame1, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5)

entry_nome = tk.Entry(frame1)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_senha = tk.Label(frame1, text="Senha:")
label_senha.grid(row=1, column=0, padx=5, pady=5)

entry_senha = tk.Entry(frame1)
entry_senha.grid(row=1, column=1, padx=5, pady=5)

frame2 = tk.LabelFrame(text='Registros')
frame2.grid(padx=(55, 0))

label_registros01 = tk.Label(frame2, text="Primeiro Registro:")
label_registros01.grid(row=0, column=0, padx=5, pady=5)

entry_registros01 = tk.Entry(frame2)
entry_registros01.grid(row=0, column=1, padx=5, pady=5)

label_registros02 = tk.Label(frame2, text="Segundo Registro:")
label_registros02.grid(row=1, column=0, padx=5, pady=5)

entry_registros02 = tk.Entry(frame2)
entry_registros02.grid(row=1, column=1, padx=5, pady=5)

window.mainloop()