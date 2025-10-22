from conexao_db import ConexaoDB
import dotenv
import os
import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

# Carrega as variáveis de ambiente (mesma conexão)
dotenv.load_dotenv(dotenv.find_dotenv())

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

# --- FUNÇÕES DE BANCO DE DADOS ---

def fetch_authors(search_term=None):
    """Busca autores, filtrando pelo termo de pesquisa se fornecido."""
    sql = "SELECT id_autor, nome_autor FROM autores"
    params = None
    
    if search_term:
        sql += " WHERE nome_autor LIKE %s"
        params = (f"%{search_term}%",)
        
    sql += " ORDER BY nome_autor ASC;"
    
    with ConexaoDB(db_config) as db:
        return db.consultar(sql, params)

# --- FUNÇÕES DE LÓGICA (CRUD) ---

def refresh_author_list(tree, ent_pesquisa):
    """Atualiza a árvore de autores com base no filtro de pesquisa."""
    search_term = ent_pesquisa.get().strip() or None
    
    # Limpa a árvore
    for row in tree.get_children():
        tree.delete(row)
        
    # Preenche com novos dados
    autores = fetch_authors(search_term)
    if autores:
        for autor in autores:
            tree.insert("", "end", values=(autor['id_autor'], autor['nome_autor']))

def limpar_campos(nome_var, ent_pesquisa, tree):
    """Limpa o campo de nome, o de pesquisa e deseleciona a árvore."""
    nome_var.set("")
    ent_pesquisa.delete(0, 'end')
    
    selection = tree.selection()
    if selection:
        tree.selection_remove(selection)
    
    # Atualiza a lista após limpar
    refresh_author_list(tree, ent_pesquisa)

def on_tree_select(event, tree, nome_var):
    """Preenche o campo de nome quando um autor é selecionado na lista."""
    selected_item = tree.selection()
    if not selected_item:
        return
    
    item = tree.item(selected_item[0], 'values')
    if item:
        # Coluna 0: id, Coluna 1: nome
        nome_var.set(item[1])

def cadastrar_autor(nome_var, ent_pesquisa, tree):
    """Cadastra um novo autor no banco de dados."""
    if tree.selection():
        messagebox.showwarning("Aviso", "Um autor está selecionado para edição.\nClique em 'Limpar' primeiro se deseja cadastrar um novo autor.")
        return

    nome = nome_var.get().strip()
    if not nome:
        messagebox.showerror("Erro", "O nome do autor é obrigatório.")
        return

    # Verifica se o autor já existe
    sql_check = "SELECT id_autor FROM autores WHERE nome_autor = %s"
    with ConexaoDB(db_config) as db:
        if db.consultar(sql_check, (nome,)):
            messagebox.showerror("Erro", "Este autor já está cadastrado.")
            return

    sql_insert = "INSERT INTO autores (nome_autor) VALUES (%s)"
    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql_insert, (nome,))
        
    if ok:
        messagebox.showinfo("Sucesso", "Autor cadastrado com sucesso!")
        limpar_campos(nome_var, ent_pesquisa, tree)
        # refresh_author_list é chamado dentro de limpar_campos
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar autor.")

def alterar_autor(nome_var, ent_pesquisa, tree):
    """Altera o nome do autor selecionado."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um autor na lista para alterar.")
        return
        
    try:
        selected_id = tree.item(selected_item[0], 'values')[0]
    except IndexError:
        messagebox.showerror("Erro", "Não foi possível obter o ID do autor.")
        return

    novo_nome = nome_var.get().strip()
    if not novo_nome:
        messagebox.showerror("Erro", "O nome do autor é obrigatório.")
        return

    # Verifica se o *novo nome* já existe (e não é o próprio autor)
    sql_check = "SELECT id_autor FROM autores WHERE nome_autor = %s AND id_autor != %s"
    with ConexaoDB(db_config) as db:
        if db.consultar(sql_check, (novo_nome, selected_id)):
            messagebox.showerror("Erro", "Este nome de autor já está em uso por outro cadastro.")
            return

    sql_update = "UPDATE autores SET nome_autor = %s WHERE id_autor = %s"
    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql_update, (novo_nome, selected_id))
        
    if ok:
        messagebox.showinfo("Sucesso", "Autor alterado com sucesso!")
        limpar_campos(nome_var, ent_pesquisa, tree)
    else:
        messagebox.showerror("Erro", "Falha ao alterar autor.")

def deletar_autor(nome_var, ent_pesquisa, tree):
    """Deleta o autor selecionado, se ele não tiver livros associados."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um autor na lista para deletar.")
        return

    try:
        item = tree.item(selected_item[0], 'values')
        selected_id = item[0]
        nome = item[1]
    except IndexError:
        messagebox.showerror("Erro", "Não foi possível obter os dados do autor.")
        return

    # --- Verificação de Integridade Referencial ---
    # Verifica se este autor está sendo usado na tabela 'livros'
    sql_check = "SELECT id_livro FROM livros WHERE autor_id = %s LIMIT 1"
    with ConexaoDB(db_config) as db:
        if db.consultar(sql_check, (selected_id,)):
            messagebox.showerror("Ação Bloqueada", f"Não é possível deletar '{nome}'.\nEste autor está associado a um ou mais livros.\nDelete os livros dele primeiro.")
            return
    # --- Fim da Verificação ---

    confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o autor '{nome}' (ID: {selected_id})?")
    if not confirm:
        return

    sql_delete = "DELETE FROM autores WHERE id_autor = %s"
    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql_delete, (selected_id,))

    if ok:
        messagebox.showinfo("Sucesso", "Autor deletado com sucesso!")
        limpar_campos(nome_var, ent_pesquisa, tree)
    else:
        messagebox.showerror("Erro", "Falha ao deletar autor.")

# --- CONSTRUÇÃO DA INTERFACE ---

def build_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Cadastro de Autores")
    app.geometry("600x400")

    frame = ctk.CTkFrame(master=app, corner_radius=8)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    # Variáveis
    nome_var = StringVar()

    # --- Campos (row 0-1) ---
    lbl_nome = ctk.CTkLabel(master=frame, text="Nome do Autor:")
    lbl_nome.grid(row=0, column=0, sticky="w", padx=(10,6), pady=(10,6))
    ent_nome = ctk.CTkEntry(master=frame, textvariable=nome_var, width=300)
    ent_nome.grid(row=0, column=1, sticky="ew", pady=(10,6))

    lbl_pesquisa = ctk.CTkLabel(master=frame, text="Pesquisar:")
    lbl_pesquisa.grid(row=1, column=0, sticky="w", padx=(10,6), pady=(6,12))
    ent_pesquisa = ctk.CTkEntry(master=frame, width=300,
                                placeholder_text="Digite um nome para filtrar...")
    ent_pesquisa.grid(row=1, column=1, sticky="ew", pady=(6,12))

    # --- Botões (row 2) ---
    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(6,12))

    # --- Treeview (row 3) ---
    tree_frame = ctk.CTkFrame(master=frame)
    tree_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=(6,10))

    # --- Configuração do Treeview ---
    columns = ("id", "nome")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome do Autor")
    tree.column("id", width=60, anchor="center")
    tree.column("nome", width=420)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # --- Configuração dos Botões ---
    cadastrar_btn = ctk.CTkButton(master=btn_frame, text="Cadastrar", width=100,
                                  command=lambda: cadastrar_autor(nome_var, ent_pesquisa, tree))
    cadastrar_btn.grid(row=0, column=0, padx=6)

    alterar_btn = ctk.CTkButton(master=btn_frame, text="Alterar", width=100,
                                command=lambda: alterar_autor(nome_var, ent_pesquisa, tree))
    alterar_btn.grid(row=0, column=1, padx=6)
    
    deletar_btn = ctk.CTkButton(master=btn_frame, text="Deletar", width=100,
                                command=lambda: deletar_autor(nome_var, ent_pesquisa, tree),
                                fg_color="#D32F2F", hover_color="#B71C1C")
    deletar_btn.grid(row=0, column=2, padx=6)
    
    limpar_btn = ctk.CTkButton(master=btn_frame, text="Limpar", width=100,
                               command=lambda: limpar_campos(nome_var, ent_pesquisa, tree),
                               fg_color="#555555", hover_color="#333333")
    limpar_btn.grid(row=0, column=3, padx=6)

    # --- Ligar Eventos ---
    ent_pesquisa.bind("<KeyRelease>", lambda event: refresh_author_list(tree, ent_pesquisa))
    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tree, nome_var))

    # --- Layout Responsivo ---
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(3, weight=1)

    # Carga inicial
    refresh_author_list(tree, ent_pesquisa)
    return app

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()