from conexao_db import ConexaoDB
import dotenv
import os
import customtkinter as ctk
from tkinter import ttk, messagebox, StringVar

dotenv.load_dotenv(dotenv.find_dotenv())

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

meuBanco = ConexaoDB(db_config)

# --- FUNÇÃO 'fetch_books' ---
def fetch_books(autor_id=None, search_term=None):
    """
    Busca livros. Filtra por autor_id E/OU search_term (no título).
    Ordena alfabeticamente pelo título.
    """
    sql = """
    SELECT 
        livros.id_livro,
        livros.titulo_livro,
        livros.ano_publicacao,
        autores.nome_autor AS autor_nome
    FROM livros
    LEFT JOIN autores ON livros.autor_id = autores.id_autor
    """
    
    # Lista para construir a cláusula WHERE dinamicamente
    where_clauses = []
    params = []
    
    if autor_id:
        where_clauses.append("livros.autor_id = %s")
        params.append(autor_id)
        
    if search_term:
        # Usa LIKE para "contém"
        where_clauses.append("livros.titulo_livro LIKE %s")
        params.append(f"%{search_term}%") 
    
    # Se houver alguma condição, junta com 'AND'
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    
    sql += " ORDER BY livros.titulo_livro ASC;" 
    
    with ConexaoDB(db_config) as db:
        # Converte a lista de params para tupla, ou passa None se estiver vazia
        return db.consultar(sql, tuple(params) if params else None)

def fetch_authors():
    sql = "SELECT id_autor, nome_autor FROM autores ORDER BY nome_autor;"
    with ConexaoDB(db_config) as db:
        return db.consultar(sql)

# --- FUNÇÃO 'limpar_campos' ---
def limpar_campos(titulo_var, ano_var, autor_nome_var, pesquisa_var, tree):
    """Limpa os campos de entrada e deseleciona qualquer item na árvore."""
    titulo_var.set("")
    ano_var.set("")
    
    # Define o padrão do combobox
    autor_nome_var.set("Mostrar todos os autores") 
    
    # Limpa o campo de pesquisa
    # Isso também vai disparar o 'trace' e atualizar a lista
    pesquisa_var.set("") 
    
    selection = tree.selection()
    if selection:
        tree.selection_remove(selection)

# --- FUNÇÃO 'cadastrar_livro' ---
def cadastrar_livro(titulo_var, ano_var, autor_nome_var, autor_map, ent_pesquisa, tree):
    if tree.selection():
        messagebox.showwarning("Aviso", "Um livro está selecionado para edição.\nClique em 'Limpar' primeiro se deseja cadastrar um novo livro.")
        return
    
    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_nome = autor_nome_var.get().strip() 

    if not titulo: messagebox.showerror("Erro", "Por favor, digite o título do livro."); return

    # 1. Verifica se o campo Ano está vazio
    if not ano:
        messagebox.showerror("Erro", "Por favor, digite o ano de publicação.")
        return
    # 2. Verifica se o campo Ano contém apenas números
    if not ano.isdigit(): 
        messagebox.showerror("Erro", "Ano inválido. Digite apenas números.")
        return
        
    autor_id = autor_map.get(autor_nome) 
    if not autor_id: messagebox.showerror("Erro", "Autor inválido ou não selecionado."); return

    sql = "INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES (%s, %s, %s);"
    params = (titulo, ano, autor_id) 

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        limpar_campos(titulo_var, ano_var, autor_nome_var, ent_pesquisa, tree)
        refresh_book_list(tree, autor_nome_var, autor_map, ent_pesquisa)
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar livro.")

# --- FUNÇÃO 'alterar_livro' ---
# Precisa de 'pesquisa_var' para passar para 'limpar_campos'
def alterar_livro(titulo_var, ano_var, autor_nome_var, autor_map, ent_pesquisa, tree):
    selected_item = tree.selection()
    if not selected_item: messagebox.showerror("Erro", "Selecione um livro na lista para alterar."); return
    try:
        id_livro = tree.item(selected_item[0], 'values')[0]
    except IndexError:
        messagebox.showerror("Erro", "Não foi possível obter o ID do livro selecionado."); return
    
    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_nome = autor_nome_var.get().strip()

    if not titulo: messagebox.showerror("Erro", "Por favor, digite o título do livro."); return

    # 1. Verifica se o campo Ano está vazio
    if not ano:
        messagebox.showerror("Erro", "Por favor, digite o ano de publicação.")
        return
    # 2. Verifica se o campo Ano contém apenas números
    if not ano.isdigit(): 
        messagebox.showerror("Erro", "Ano inválido. Digite apenas números.")
        return
    # --- FIM DA MUDANÇA ---
        
    autor_id = autor_map.get(autor_nome)
    if not autor_id: messagebox.showerror("Erro", "Autor inválido ou não selecionado."); return

    confirm = messagebox.askyesno("Confirmar Alteração", f"Salvar alterações para o livro ID: {id_livro}?")
    if not confirm: return

    sql = "UPDATE livros SET titulo_livro = %s, ano_publicacao = %s, autor_id = %s WHERE id_livro = %s;"
    params = (titulo, ano, autor_id, id_livro)

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro alterado com sucesso!")
        limpar_campos(titulo_var, ano_var, autor_nome_var, ent_pesquisa, tree)
        refresh_book_list(tree, autor_nome_var, autor_map, ent_pesquisa)
    else:
        messagebox.showerror("Erro", "Falha ao alterar livro.")

# --- FUNÇÃO 'deletar_livro' ---
# Precisa de 'pesquisa_var' para passar para 'limpar_campos'
def deletar_livro(tree, titulo_var, ano_var, autor_nome_var, pesquisa_var):
    selected_item = tree.selection() 
    if not selected_item:
        messagebox.showerror("Erro", "Por favor, selecione um livro na lista para deletar.")
        return

    item_id_tree = selected_item[0] 
    try:
        values = tree.item(item_id_tree, 'values')
        id_livro = values[0]
        titulo_livro = values[1]
    except IndexError:
        messagebox.showerror("Erro", "Não foi possível obter os dados do livro selecionado.")
        return

    confirm = messagebox.askyesno(
        "Confirmar Exclusão", 
        f"Tem certeza que deseja deletar o livro:\n\n'{titulo_livro}' (ID: {id_livro})?"
    )
    if not confirm:
        return 

    sql = "DELETE FROM livros WHERE id_livro = %s;"
    params = (id_livro,)

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro deletado com sucesso!")
        limpar_campos(titulo_var, ano_var, autor_nome_var, pesquisa_var, tree) 
    else:
        messagebox.showerror("Erro", "Falha ao deletar o livro.")

# --- FUNÇÃO 'refresh_tree' ---
def refresh_tree(tree, autor_id=None, search_term=None):
    """
    Atualiza a árvore. Filtra por autor_id E/OU search_term.
    """
    for row in tree.get_children():
        tree.delete(row)
    
    # Chama a função fetch_books (agora modificada)
    livros = fetch_books(autor_id=autor_id, search_term=search_term) 
    
    if livros:
        for livro in livros:
            tree.insert("", "end", values=(
                livro['id_livro'],
                livro['titulo_livro'],
                livro.get('ano_publicacao') or "—", 
                livro.get('autor_nome') or "—"    
            ))

def on_tree_select(event, tree, titulo_var, ano_var, autor_nome_var):
    selected_item = tree.selection()
    if not selected_item:
        return
    
    item = tree.item(selected_item[0], 'values')
    if not item:
        return
        
    titulo_var.set(item[1])
    ano_var.set(item[2] if item[2] != "—" else "") 
    
    autor_selecionado = item[3]
    if autor_selecionado != "—":
        autor_nome_var.set(autor_selecionado)
    else:
        autor_nome_var.set("Mostrar todos os autores")

# --- NOVA FUNÇÃO CENTRALIZADA PARA ATUALIZAR A LISTA ---
def refresh_book_list(tree, autor_nome_var, autor_map, pesquisa_var):
    """Pega os filtros atuais (autor e pesquisa) e atualiza a árvore."""
    
    # 1. Pega o ID do Autor
    selected_name = autor_nome_var.get()
    autor_id = None
    if selected_name == "Mostrar todos os autores":
        autor_id = None
    elif selected_name in autor_map:
        autor_id = autor_map.get(selected_name)
    
    # 2. Pega o Termo de Pesquisa
    search_term = pesquisa_var.get().strip()
    if not search_term:
        search_term = None # Trata string vazia como "sem pesquisa"
        
    # 3. Chama a função de atualização
    refresh_tree(tree, autor_id=autor_id, search_term=search_term)
    
def build_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Cadastro de Livros")
    app.geometry("800x900+500+50") # Define tamanho inicial(900x600) e posição (450+150)

    frame = ctk.CTkFrame(master=app, corner_radius=8)
    frame.pack(fill="both", expand=True, padx=12, pady=12)

    autores_data = fetch_authors()
    autor_map = {}
    if autores_data:
        autor_map = {autor['nome_autor']: autor['id_autor'] for autor in autores_data}
    
    autor_nomes = list(autor_map.keys())
    if not autor_nomes:
        autor_nomes = ["Nenhum autor cadastrado"] 
    else:
        autor_nomes.insert(0, "Mostrar todos os autores")

    # Variáveis de controle
    titulo_var = StringVar()
    ano_var = StringVar()
    autor_nome_var = StringVar() 
    pesquisa_var = StringVar()

    # --- CAMPOS DE CADASTRO/ALTERAÇÃO 
    lbl_titulo = ctk.CTkLabel(master=frame, text="Título:")
    lbl_titulo.grid(row=0, column=0, sticky="w", padx=(10,6), pady=(10,6))
    ent_titulo = ctk.CTkEntry(master=frame, textvariable=titulo_var, width=420)
    ent_titulo.grid(row=0, column=1, sticky="ew", pady=(10,6))

    lbl_ano = ctk.CTkLabel(master=frame, text="Ano:")
    lbl_ano.grid(row=1, column=0, sticky="w", padx=(10,6), pady=6)
    ent_ano = ctk.CTkEntry(master=frame, textvariable=ano_var, width=200)
    ent_ano.grid(row=1, column=1, sticky="w", pady=6)

    lbl_autor = ctk.CTkLabel(master=frame, text="Autor:") 
    lbl_autor.grid(row=2, column=0, sticky="w", padx=(10,6), pady=6)
    
    cmb_autor = ctk.CTkComboBox(master=frame, 
                                variable=autor_nome_var, 
                                values=autor_nomes,
                                width=200,
                                state="readonly",
                                command=lambda value: refresh_book_list(
                                    tree, autor_nome_var, autor_map, pesquisa_var
                                ))
    cmb_autor.grid(row=2, column=1, sticky="w", pady=6)
    cmb_autor.set("Mostrar todos os autores") 
    
    lbl_pesquisa = ctk.CTkLabel(master=frame, text="Pesquisar:")
    lbl_pesquisa.grid(row=3, column=0, sticky="w", padx=(10,6), pady=(6,12))
    ent_pesquisa = ctk.CTkEntry(master=frame, textvariable=pesquisa_var, width=200,
                                placeholder_text="Digite um título para filtrar...")
    ent_pesquisa.grid(row=3, column=1,sticky="w", pady=(6,12))
    
    # 'write' é chamado toda vez que o texto muda (usuário digita ou apaga)
    pesquisa_var.trace_add("write", lambda *args: refresh_book_list(
        tree, autor_nome_var, autor_map, pesquisa_var
    ))
    # --- FIM DO CAMPO DE PESQUISA ---

    # --- BOTÕES 
    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(6,12))

    # --- TREEVIEW 
    tree_frame = ctk.CTkFrame(master=frame)
    tree_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=(6,10))

    # --- BOTÕES (configuração) ---
    cadastrar_btn = ctk.CTkButton(master=btn_frame, text="Cadastrar 📝", width=140,
                                  command=lambda: cadastrar_livro(
                                      titulo_var, ano_var, autor_nome_var, autor_map, pesquisa_var, tree
                                  ))
    cadastrar_btn.grid(row=0, column=0, padx=6)

    alterar_btn = ctk.CTkButton(master=btn_frame, text="Alterar 🔃", width=140,
                                  command=lambda: alterar_livro(
                                      titulo_var, ano_var, autor_nome_var, autor_map, pesquisa_var, tree
                                  ))
    alterar_btn.grid(row=0, column=1, padx=6)
    
    deletar_btn = ctk.CTkButton(master=btn_frame, 
                                text="Deletar ❌", 
                                width=140,
                                command=lambda: deletar_livro(tree, titulo_var, ano_var, autor_nome_var, pesquisa_var),
                                fg_color="#D32F2F",    
                                hover_color="#B71C1C") 
    deletar_btn.grid(row=0, column=2, padx=6)
    
    limpar_btn = ctk.CTkButton(master=btn_frame,
                               text="Limpar ⟳",
                               width=140,
                               command=lambda: limpar_campos(titulo_var, ano_var, autor_nome_var, pesquisa_var, tree),
                               fg_color="#555555",
                               hover_color="#333333")
    limpar_btn.grid(row=0, column=3, padx=6)

    # --- TREEVIEW (configuração) ---
    columns = ("id", "titulo", "ano", "autor")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("titulo", text="Título")
    tree.heading("ano", text="Ano")
    tree.heading("autor", text="Autor")
    tree.column("id", width=60, anchor="center")
    tree.column("titulo", width=420)
    tree.column("ano", width=80, anchor="center")
    tree.column("autor", width=220)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tree, titulo_var, ano_var, autor_nome_var))

    # --- LAYOUT RESPONSIVO ---
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(5, weight=1) 

    # Carrega a lista inicial (mostrando todos, sem pesquisa)
    refresh_book_list(tree, autor_nome_var, autor_map, pesquisa_var)
    return app

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()
    