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

def fetch_books(autor_id=None):
    sql = """
    SELECT 
        livros.id_livro,
        livros.titulo_livro,
        livros.ano_publicacao,
        autores.nome_autor AS autor_nome
    FROM livros
    LEFT JOIN autores ON livros.autor_id = autores.id_autor
    """

    params = None
    if autor_id:
        sql += " WHERE livros.autor_id = %s"
        params = (autor_id,)

    sql += " ORDER BY livros.titulo_livro ASC;"

    with ConexaoDB(db_config) as db:
        return db.consultar(sql, params)

def fetch_authors():
    sql = "SELECT id_autor, nome_autor FROM autores ORDER BY nome_autor;"
    with ConexaoDB(db_config) as db:
        return db.consultar(sql)

def limpar_campos(titulo_var, ano_var, autor_nome_var, tree):
    """Limpa os campos de entrada e deseleciona qualquer item na árvore."""
    titulo_var.set("")
    ano_var.set("")
    
    # Define o padrão do combobox para "Mostrar todos os livros"
    autor_nome_var.set("Mostrar todos os autores") 
    
    selection = tree.selection()
    if selection:
        tree.selection_remove(selection)

def cadastrar_livro(titulo_var, ano_var, autor_nome_var, autor_map, tree):
    if tree.selection():
        messagebox.showwarning("Aviso", "Um livro está selecionado para edição.\nClique em 'Limpar' primeiro se deseja cadastrar um novo livro.")
        return

    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_nome = autor_nome_var.get().strip() 

    if not titulo:
        messagebox.showerror("Erro", "Título é obrigatório.")
        return
    if ano and not ano.isdigit():
        messagebox.showerror("Erro", "Ano inválido.")
        return
 
    autor_id = autor_map.get(autor_nome) 
    if not autor_id:
        messagebox.showerror("Erro", "Autor inválido ou não selecionado.")
        return

    sql = "INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES (%s, %s, %s);"
    params = (titulo, ano if ano else None, autor_id) 

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        limpar_campos(titulo_var, ano_var, autor_nome_var, tree) 
        # Atualiza a árvore (mostrando todos, pois autor_id=None por padrão)
        refresh_tree(tree) 
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar livro.")

def alterar_livro(titulo_var, ano_var, autor_nome_var, autor_map, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um livro na lista para alterar.")
        return

    try:
        item_values = tree.item(selected_item[0], 'values')
        id_livro = item_values[0]
    except IndexError:
        messagebox.showerror("Erro", "Não foi possível obter o ID do livro selecionado.")
        return

    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_nome = autor_nome_var.get().strip()

    if not titulo:
        messagebox.showerror("Erro", "Título é obrigatório.")
        return
    if ano and not ano.isdigit():
        messagebox.showerror("Erro", "Ano inválido.")
        return
    
    autor_id = autor_map.get(autor_nome)
    if not autor_id:
        messagebox.showerror("Erro", "Autor inválido ou não selecionado.")
        return

    confirm = messagebox.askyesno(
        "Confirmar Alteração", 
        f"Tem certeza que deseja salvar as alterações para o livro ID: {id_livro}?"
    )
    if not confirm:
        return

    sql = "UPDATE livros SET titulo_livro = %s, ano_publicacao = %s, autor_id = %s WHERE id_livro = %s;"
    params = (titulo, ano if ano else None, autor_id, id_livro)

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro alterado com sucesso!")
        limpar_campos(titulo_var, ano_var, autor_nome_var, tree) 
        refresh_tree(tree) # Atualiza mostrando todos
    else:
        messagebox.showerror("Erro", "Falha ao alterar livro.")

def deletar_livro(tree, titulo_var, ano_var, autor_nome_var):
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
        limpar_campos(titulo_var, ano_var, autor_nome_var, tree) 
        refresh_tree(tree) # Atualiza mostrando todos
    else:
        messagebox.showerror("Erro", "Falha ao deletar o livro.")

def refresh_tree(tree, autor_id=None):
    """
    Atualiza a árvore. Se 'autor_id' for fornecido, filtra por esse autor.
    """
    for row in tree.get_children():
        tree.delete(row)
    
    # Chama a função fetch_books 
    livros = fetch_books(autor_id=autor_id) 
    
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
        # Se o livro não tiver autor, reseta o combobox para o padrão
        autor_nome_var.set("Mostrar todos os autores")

def on_author_filter_changed(selected_name, autor_map, tree):
    """Filtra a árvore de livros com base no autor selecionado no combobox."""
    
    autor_id = None
    if selected_name == "Mostrar todos os autores":
        autor_id = None
    elif selected_name in autor_map:
        autor_id = autor_map.get(selected_name)
    else:
        return 

    # Chama refresh_tree com o ID do autor (ou None)
    refresh_tree(tree, autor_id=autor_id)

def build_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Cadastro de Livros")
    app.geometry("900x420")

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

    titulo_var = StringVar()
    ano_var = StringVar()
    autor_nome_var = StringVar() 

    lbl_titulo = ctk.CTkLabel(master=frame, text="Título:")
    lbl_titulo.grid(row=0, column=0, sticky="w", padx=(10,6), pady=(10,6))
    ent_titulo = ctk.CTkEntry(master=frame, textvariable=titulo_var, width=420)
    ent_titulo.grid(row=0, column=1, sticky="ew", pady=(10,6))

    lbl_ano = ctk.CTkLabel(master=frame, text="Ano:")
    lbl_ano.grid(row=1, column=0, sticky="w", padx=(10,6), pady=6)
    ent_ano = ctk.CTkEntry(master=frame, textvariable=ano_var, width=170)
    ent_ano.grid(row=1, column=1, sticky="w", pady=6)

    lbl_autor = ctk.CTkLabel(master=frame, text="Autor:") 
    lbl_autor.grid(row=2, column=0, sticky="w", padx=(10,6), pady=6)

    # Adicionado o parâmetro 'command'
    cmb_autor = ctk.CTkComboBox(master=frame, 
                                variable=autor_nome_var, 
                                values=autor_nomes,
                                width=200,
                                state="readonly",
                                command=lambda value: on_author_filter_changed(
                                    value, autor_map, tree
                                ))
 
    cmb_autor.grid(row=2, column=1, sticky="w", pady=6)
    # Define o novo valor padrão
    cmb_autor.set("Mostrar todos os autores") 

    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(6,12))

    tree_frame = ctk.CTkFrame(master=frame)
    tree_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(6,10))

    cadastrar_btn = ctk.CTkButton(master=btn_frame, text="Cadastrar", width=140,
                                  command=lambda: cadastrar_livro(
                                      titulo_var, ano_var, autor_nome_var, autor_map, tree
                                  ))
    cadastrar_btn.grid(row=0, column=0, padx=6)

    alterar_btn = ctk.CTkButton(master=btn_frame, text="Alterar", width=140,
                                  command=lambda: alterar_livro(
                                      titulo_var, ano_var, autor_nome_var, autor_map, tree
                                  ))
    alterar_btn.grid(row=0, column=1, padx=6)
    
    deletar_btn = ctk.CTkButton(master=btn_frame, 
                                text="Deletar", 
                                width=140,
                                command=lambda: deletar_livro(tree, titulo_var, ano_var, autor_nome_var),
                                fg_color="#D32F2F",    
                                hover_color="#B71C1C") 
    deletar_btn.grid(row=0, column=2, padx=6)

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

    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(4, weight=1)

    # Carrega a lista inicial (mostrando todos)
    refresh_tree(tree) 
    return app

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()