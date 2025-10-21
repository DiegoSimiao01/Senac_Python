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

def fetch_books():
    sql = """
    SELECT 
        livros.id_livro,
        livros.titulo_livro,
        livros.ano_publicacao,
        autores.nome_autor AS autor_nome
    FROM livros
    LEFT JOIN autores ON livros.autor_id = autores.id_autor
    ORDER BY livros.id_livro;
    """
    with ConexaoDB(db_config) as db:
        return db.consultar(sql)

def fetch_authors():
    """Busca todos os autores para popular o combobox."""
    sql = "SELECT id_autor, nome_autor FROM autores ORDER BY nome_autor;"
    with ConexaoDB(db_config) as db:
        return db.consultar(sql)

def cadastrar_livro(titulo_var, ano_var, autor_nome_var, autor_map, tree):
    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_nome = autor_nome_var.get().strip() 

    if not titulo:
        messagebox.showerror("Erro", "Título é obrigatório.")
        return

    if ano and not ano.isdigit():
        messagebox.showerror("Erro", "Ano inválido.")
        return

    autor_id = None
    if autor_nome and autor_nome != "Selecione um autor":
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
        titulo_var.set("")
        ano_var.set("")
        autor_nome_var.set("Selecione um autor") 
        refresh_tree(tree)
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar livro.")

def deletar_livro(tree):
    """Deleta o livro selecionado no Treeview."""
    
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
        refresh_tree(tree) 
    else:
        messagebox.showerror("Erro", "Falha ao deletar o livro.")

def refresh_tree(tree):
    for row in tree.get_children():
        tree.delete(row)
    livros = fetch_books()
    if livros:
        for livro in livros:
            tree.insert("", "end", values=(
                livro['id_livro'],
                livro['titulo_livro'],
                livro.get('ano_publicacao') or "—", 
                livro.get('autor_nome') or "—"    
            ))

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

    titulo_var = StringVar()
    ano_var = StringVar()
    autor_nome_var = StringVar() 

    lbl_titulo = ctk.CTkLabel(master=frame, text="Título:")
    lbl_titulo.grid(row=0, column=0, sticky="w", padx=(10,6), pady=(10,6))
    ent_titulo = ctk.CTkEntry(master=frame, placeholder_text="Título do livro", width=420)
    ent_titulo.grid(row=0, column=1, sticky="ew", pady=(10,6))

    lbl_ano = ctk.CTkLabel(master=frame, text="Ano:")
    lbl_ano.grid(row=1, column=0, sticky="w", padx=(10,6), pady=6)
    ent_ano = ctk.CTkEntry(master=frame, placeholder_text="Ano de publicação", width=150)
    ent_ano.grid(row=1, column=1, sticky="w", pady=6)

    lbl_autor = ctk.CTkLabel(master=frame, text="Autor:") 
    lbl_autor.grid(row=2, column=0, sticky="w", padx=(10,6), pady=6)
   
    cmb_autor = ctk.CTkComboBox(master=frame, 
                                variable=autor_nome_var, 
                                values=autor_nomes,
                                width=300,
                                state="readonly")  # Adicionado state="readonly"

    cmb_autor.grid(row=2, column=1, sticky="w", pady=6)
    cmb_autor.set("Selecione um autor") 

    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(6,12))

    tree_frame = ctk.CTkFrame(master=frame)
    tree_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(6,10))

    cadastrar_btn = ctk.CTkButton(master=btn_frame, text="Cadastrar", width=120,
                                  command=lambda: cadastrar_livro(
                                      titulo_var, 
                                      ano_var, 
                                      autor_nome_var,
                                      autor_map,
                                      tree
                                  ))
    cadastrar_btn.grid(row=0, column=0, padx=6)

    atualizar_btn = ctk.CTkButton(master=btn_frame, text="Atualizar lista", width=140,
                                  command=lambda: refresh_tree(tree))
    atualizar_btn.grid(row=0, column=1, padx=6)
    
    deletar_btn = ctk.CTkButton(master=btn_frame, 
                                text="Deletar Selecionado", 
                                width=160,
                                command=lambda: deletar_livro(tree),
                                fg_color="#D32F2F",    
                                hover_color="#B71C1C") 
    deletar_btn.grid(row=0, column=2, padx=6)

    columns = ("ID", "Título", "Ano", "Autor")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    tree.heading("ID", text="ID Livro")
    tree.heading("Título", text="Título")
    tree.heading("Ano", text="Ano")
    tree.heading("Autor", text="Autor")
    tree.column("ID", width=60, anchor="center")
    tree.column("Título", width=420)
    tree.column("Ano", width=80, anchor="center")
    tree.column("Autor", width=220)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(4, weight=1)

    refresh_tree(tree)
    return app

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()