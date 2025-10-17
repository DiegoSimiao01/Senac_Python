# ...existing code...
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

def cadastrar_livro(titulo_var, ano_var, autor_id_var, tree):
    titulo = titulo_var.get().strip()
    ano = ano_var.get().strip()
    autor_id = autor_id_var.get().strip()

    if not titulo:
        messagebox.showerror("Erro", "Título é obrigatório.")
        return

    if ano and not ano.isdigit():
        messagebox.showerror("Erro", "Ano inválido.")
        return

    if autor_id and not autor_id.isdigit():
        messagebox.showerror("Erro", "ID do autor inválido.")
        return

    sql = "INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES (%s, %s, %s);"
    params = (titulo, ano if ano else None, autor_id if autor_id else None)

    with ConexaoDB(db_config) as db:
        ok = db.manipular(sql, params)

    if ok:
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        titulo_var.set("")
        ano_var.set("")
        autor_id_var.set("")
        refresh_tree(tree)
    else:
        messagebox.showerror("Erro", "Falha ao cadastrar livro.")

def refresh_tree(tree):
    for row in tree.get_children():
        tree.delete(row)
    livros = fetch_books()
    if livros:
        for livro in livros:
            tree.insert("", "end", values=(
                livro['id_livro'],
                livro['titulo_livro'],
                livro.get('ano_publicacao'),
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

    # Labels e Entradas
    titulo_var = StringVar()
    ano_var = StringVar()
    autor_id_var = StringVar()

    lbl_titulo = ctk.CTkLabel(master=frame, text="Título:")
    lbl_titulo.grid(row=0, column=0, sticky="w", padx=(10,6), pady=(10,6))
    ent_titulo = ctk.CTkEntry(master=frame, textvariable=titulo_var, width=420)
    ent_titulo.grid(row=0, column=1, sticky="ew", pady=(10,6))

    lbl_ano = ctk.CTkLabel(master=frame, text="Ano:")
    lbl_ano.grid(row=1, column=0, sticky="w", padx=(10,6), pady=6)
    ent_ano = ctk.CTkEntry(master=frame, textvariable=ano_var, width=150)
    ent_ano.grid(row=1, column=1, sticky="w", pady=6)

    lbl_autor = ctk.CTkLabel(master=frame, text="ID do Autor:")
    lbl_autor.grid(row=2, column=0, sticky="w", padx=(10,6), pady=6)
    ent_autor = ctk.CTkEntry(master=frame, textvariable=autor_id_var, width=150)
    ent_autor.grid(row=2, column=1, sticky="w", pady=6)

    # Botões
    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(6,12))

    tree_frame = ctk.CTkFrame(master=frame)
    tree_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=10, pady=(6,10))

    cadastrar_btn = ctk.CTkButton(master=btn_frame, text="Cadastrar", width=120,
                                  command=lambda: cadastrar_livro(titulo_var, ano_var, autor_id_var, tree))
    cadastrar_btn.grid(row=0, column=0, padx=6)

    atualizar_btn = ctk.CTkButton(master=btn_frame, text="Atualizar lista", width=140,
                                  command=lambda: refresh_tree(tree))
    atualizar_btn.grid(row=0, column=1, padx=6)

    # Treeview (usando ttk para colunas) - agora com Autor
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

    # layout responsivo
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(4, weight=1)

    refresh_tree(tree)
    return app

if __name__ == "__main__":
    app = build_gui()
    app.mainloop()
# ...existing code...