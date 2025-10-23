# Sistema Biblioteca — Cadastro de Livros (GUI)

Pequeno aplicativo Tk/CustomTkinter para gerenciar livros: listar, cadastrar, alterar, deletar e filtrar por autor ou título.

## Funcionalidades
- Listagem de livros com: ID, Título, Ano e Autor.
- Cadastro de novos livros.
- Edição e exclusão de livros.
- Filtro por autor (combobox) e pesquisa por título (campo dinamicamente atualiza a lista).
- Ícones (opcional) para botões.

## Pré-requisitos
- Python 3.8+ (testado em 3.10/3.12)
- Virtualenv recomendado

## Dependências
Instale em um ambiente virtual:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install customtkinter pillow python-dotenv mysql-connector-python
```

A biblioteca de banco pode variar conforme `ConexaoDB`. Se sua `ConexaoDB` usa outro driver (psycopg2, sqlite3, etc.) instale-o também.

Você pode criar um `requirements.txt` com:
```
customtkinter
Pillow
python-dotenv
mysql-connector-python
```

## Variáveis de ambiente
Crie um arquivo `.env` na mesma pasta com as credenciais do banco:

```
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_DATABASE=nome_do_banco
```

O código carrega essas variáveis via python-dotenv.

## Estrutura esperada
- cadastroLivros.py — GUI principal
- conexao_db.py — wrapper de conexão e métodos `consultar` / `manipular`
- icons/add.png — (opcional) ícone usado no botão cadastrar

Coloque o PNG em `Sistema_Biblioteca/icons/add.png` se quiser o ícone.

## Observações / Solução de problemas
- Erro `ImportError: cannot import name 'ctk_tkinter'`: importe corretamente com `import customtkinter as ctk`.
- Se houver erro na conexão com o banco, verifique `.env` e a implementação de `ConexaoDB`.
- Se o treeview não mostra colunas do autor, confirme que a query faz `LEFT JOIN autores` e retorna `autor_nome`.
- Para ícones, use PNGs pequenos (18–24 px). Se não existir o arquivo de ícone, o botão continuará funcionando sem imagem.

## Personalização rápida
- Alterar aparência: `ctk.set_appearance_mode("System" | "Dark" | "Light")`
- Alterar tema: `ctk.set_default_color_theme("blue")` ou caminho para arquivo de tema.

## Licença
Código fornecido sem licença explícita — adapte conforme necessário.

