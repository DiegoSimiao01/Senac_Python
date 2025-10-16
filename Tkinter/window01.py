import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Necessário instalar: pip install pillow

# --- Funções de Ação ---

def entrar():
    cpf = entry_cpf.get()
    senha = entry_senha.get()
    # Lógica de login simples (exemplo)
    if cpf == "12345678900" and senha == "senha123":
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
    else:
        messagebox.showerror("Erro", "CPF ou Senha inválidos.")

def cadastrar_se():
    messagebox.showinfo("Cadastro", "A tela de cadastro seria aberta aqui.")

def esqueci_minha_senha():
    messagebox.showinfo("Recuperação", "O processo de recuperação de senha seria iniciado aqui.")

def toggle_password_visibility():
    """Alterna entre mostrar e ocultar a senha."""
    if entry_senha.cget('show') == '*':
        entry_senha.config(show='')
        btn_toggle.config(image=icon_hide)
    else:
        entry_senha.config(show='*')
        btn_toggle.config(image=icon_show)

# --- Configuração Principal ---

root = tk.Tk()
root.title("Sistema de chamados")
root.geometry("350x550") # Tamanho similar a uma tela de celular
root.resizable(False, False)
root.configure(bg='white')

# --- Estilos de Cores ---
SENAC_ORANGE = "#221EF7"
SENAC_DARK_BLUE = '#003366'
FIELD_COLOR = '#F0F0F0' # Cor para o fundo dos campos

# --- Frame Central para centralizar o conteúdo ---
main_frame = tk.Frame(root, bg='white', padx=20, pady=20)
main_frame.pack(expand=True, fill='both')

# --- Logo (Simulado ou carregado) ---
try:
    # Tenta carregar uma imagem do logo (substitua 'logo_senac.png' pelo seu arquivo real)
    # Você precisará ter o arquivo do logo e a biblioteca Pillow instalada.
    logo_img = Image.open("senacbranco.png").resize((180, 70))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(main_frame, image=logo_tk, bg='blue')
    logo_label.grid(row=0, column=0, columnspan=2, pady=(30, 40))
except FileNotFoundError:
    # Texto simples se a imagem não for encontrada
    logo_label = tk.Label(main_frame, text="CHRISTUS", font=("Arial", 30, "bold"), fg=SENAC_DARK_BLUE, bg='white')
    logo_label.grid(row=0, column=0, columnspan=2, pady=(30, 40))

# --- Rótulo Login ---
label_login = tk.Label(main_frame, text="Login", font=("Arial", 20), fg=SENAC_ORANGE, bg='white')
label_login.grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 20))
# Linha de separação abaixo de "Login"
tk.Frame(main_frame, height=2, bg=SENAC_ORANGE).grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 30))

# --- Campo CPF ---
label_cpf = tk.Label(main_frame, text="CPF *", font=("Arial", 10), fg='black', bg='white')
label_cpf.grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=(0, 5))

entry_cpf = tk.Entry(main_frame, font=("Arial", 14), bd=0, relief="flat", bg=FIELD_COLOR, highlightthickness=0)
entry_cpf.grid(row=4, column=0, columnspan=2, sticky='ew', ipady=8, padx=5, pady=(0, 20))
# Linha visual abaixo do campo (como na imagem)
tk.Frame(main_frame, height=1, bg='lightgray').grid(row=5, column=0, columnspan=2, sticky='ew')

# --- Campo Senha ---
label_senha = tk.Label(main_frame, text="Senha *", font=("Arial", 10), fg='black', bg='white')
label_senha.grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=(15, 5))

# Frame para agrupar o campo de senha e o botão de toggle
senha_frame = tk.Frame(main_frame, bg=FIELD_COLOR, bd=0, relief="flat")
senha_frame.grid(row=7, column=0, columnspan=2, sticky='ew', ipady=8, padx=5)

entry_senha = tk.Entry(senha_frame, font=("Arial", 14), show='*', bd=0, relief="flat", bg=FIELD_COLOR)
entry_senha.pack(side=tk.LEFT, fill='x', expand=True, ipady=0)

# Simulação de ícones de Olho (necessita de imagens reais ou usar texto/fontes de ícone)
try:
    # Criando um ícone simples como um placeholder
    icon_show_img = Image.new('RGB', (20, 15), 'white')
    icon_hide_img = Image.new('RGB', (20, 15), 'white')
    
    # Desenhe algo que simule um olho aberto/fechado se quiser
    # Neste exemplo, usaremos texto para simplicidade se não tiver a imagem
    
    # Placeholder: você pode criar suas imagens de ícones de olho (show/hide)
    # ou usar uma fonte que contenha ícones (ex: Font Awesome)
    
    icon_show = ImageTk.PhotoImage(icon_show_img)
    icon_hide = ImageTk.PhotoImage(icon_hide_img)

    btn_toggle = tk.Button(senha_frame, text="👁️", command=toggle_password_visibility, bd=0, bg=FIELD_COLOR, fg='gray')
except:
    # Caso não consiga usar a Pillow, usa um botão simples com texto
    icon_show = "Ocultar"
    icon_hide = "Mostrar"
    btn_toggle = tk.Button(senha_frame, text="Ocultar", command=toggle_password_visibility, bd=0, bg=FIELD_COLOR, fg='gray', font=("Arial", 8))
    
btn_toggle.pack(side=tk.RIGHT, padx=5)
entry_senha.config(show='*') # Garante que comece oculto

# Linha visual abaixo do campo
tk.Frame(main_frame, height=1, bg='lightgray').grid(row=8, column=0, columnspan=2, sticky='ew')

# --- Link "Esqueci minha senha" ---
btn_esqueci_senha = tk.Button(main_frame, text="Esqueci minha senha", command=esqueci_minha_senha, fg=SENAC_DARK_BLUE, bg='white', bd=0, font=("Arial", 9))
btn_esqueci_senha.grid(row=9, column=1, sticky='e', pady=(5, 40))

# --- Botões de Ação ---

# Botão Cadastrar-se (Laranja)
btn_cadastrar = tk.Button(main_frame, text="Cadastrar-se", command=cadastrar_se, bg=SENAC_ORANGE, fg='white', font=("Arial", 12, "bold"), bd=0, relief="flat", padx=20, pady=10)
btn_cadastrar.grid(row=10, column=0, sticky='ew', padx=(5, 10))

# Botão Entrar (Azul Escuro)
btn_entrar = tk.Button(main_frame, text="Entrar", command=entrar, bg=SENAC_DARK_BLUE, fg='white', font=("Arial", 12, "bold"), bd=0, relief="flat", padx=20, pady=10)
btn_entrar.grid(row=10, column=1, sticky='ew', padx=(10, 5))

# --- Loop Principal ---
main_frame.grid_columnconfigure(0, weight=1) # Faz a primeira coluna expandir
main_frame.grid_columnconfigure(1, weight=1) # Faz a segunda coluna expandir

root.mainloop()