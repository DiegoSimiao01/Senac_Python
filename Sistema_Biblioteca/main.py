import dotenv
import os
from conexao_db import ConexaoDB # Importa a nossa nova classe

# Carrega as variáveis de ambiente (sem mudanças aqui)
dotenv.load_dotenv(dotenv.find_dotenv())

# Configuração do banco (sem mudanças aqui)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

## FUNÇÕES DO SISTEMA (AGORA MUITO MAIS LIMPAS)

def verLivros():
    sql = "SELECT id_livro, titulo_livro, ano_publicacao FROM livros;"
    with ConexaoDB(db_config) as db:
        livros = db.consultar(sql)
        if livros:
            print("\nLista de Livros:")
            for livro in livros:
                print(f"ID: {livro['id_livro']} | Título: {livro['titulo_livro']} | Ano: {livro['ano_publicacao']}")
        else:
            print("Nenhum livro encontrado.")

def cadastrarLivros():
    titulo = input("Título do Livro: ")
    ano = input("Ano de Publicação: ")
    autor_id = input("ID do Autor: ")
    
    sql = "INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES (%s, %s, %s);"
    params = (titulo, ano, autor_id)

    with ConexaoDB(db_config) as db:
        if db.manipular(sql, params):
            print("\nLivro cadastrado com sucesso!")
        else:
            print("\nFalha ao cadastrar livro.")

def verClientes():
    sql = "SELECT * FROM clientes;"
    with ConexaoDB(db_config) as db:
        clientes = db.consultar(sql)
        if clientes:
            print("\nLista de Clientes:")
            for cliente in clientes:
                print(f"ID: {cliente['id_cliente']} | Nome: {cliente['nome_cliente']} | Email: {cliente['email']} | CPF: {cliente['cpf_cliente']}")
        else:
            print("Nenhum cliente encontrado.")

def verAutores():
    sql = "SELECT * FROM autores;"
    with ConexaoDB(db_config) as db:
        autores = db.consultar(sql)
        if autores:
            print("\nLista de Autores:")
            for autor in autores:
                print(f"ID: {autor['id_autor']} | Nome: {autor['nome_autor']}")
        else:
            print("Nenhum autor encontrado.")

def verAlugueis():
    sql = """
    SELECT 
        id_aluguel,
        titulo_livro,
        nome_cliente,
        data_aluguel,
        data_devolucao
    FROM aluguel
    JOIN livros ON id_livro = livro_id
    JOIN clientes ON id_cliente = cliente_id;
    """
    
    with ConexaoDB(db_config) as db:
        alugueis = db.consultar(sql)
        if alugueis:
            print("\nLista de Alugueis:")
            for aluguel in alugueis:
                print(f"ID: {aluguel['id_aluguel']} | Livro: {aluguel['titulo_livro']} | Cliente: {aluguel['nome_cliente']} | Data Aluguel: {aluguel['data_aluguel']} | Devolução: {aluguel['data_devolucao']}")
        else:
            print("Nenhum aluguel encontrado.")

def cadastrarCliente():
    nome = input("Nome do Cliente: ")
    email = input("Email: ")
    cpf = input("CPF '11 dígitos': ")
    
    sql = "INSERT INTO clientes (nome_cliente, email, cpf_cliente) VALUES (%s, %s, %s);"
    params = (nome, email if email else None, cpf)
    
    with ConexaoDB(db_config) as db:
        if db.manipular(sql, params):
            print("\nCliente cadastrado com sucesso!")
        else:
            print("\nFalha ao cadastrar cliente.")

def cadastrarAutor():
    nome = input("Nome do Autor: ")
    sql = "INSERT INTO autores (nome_autor) VALUES (%s);"
    params = (nome,)
    
    with ConexaoDB(db_config) as db:
        if db.manipular(sql, params):
            print("\nAutor cadastrado com sucesso!")
        else:
            print("\nFalha ao cadastrar autor.")

def cadastrarAluguel():
    # 1. Exibir lista de clientes
    # 2. Pedir ao usuario o ID do cliente que alugou
    # 3. Exibir lista de livros 
    # 4. Pedir ao usuario o ID do livro, alugado 
    # 5. Executar SQL de inserção do novo aluguel
    
    verClientes()
    cliente_id = input("ID do Cliente: ")
    
    verLivros()
    livro_id = input("ID do Livro: ")
    data_aluguel = input("Data de Aluguel (AAAA-MM-DD): ")

    sql = "INSERT INTO aluguel (livro_id, cliente_id, data_aluguel) VALUES (%s, %s, %s);"
    params = (livro_id, cliente_id, data_aluguel)
    
    with ConexaoDB(db_config) as db:
        if db.manipular(sql, params):
            print("\nAluguel cadastrado com sucesso!")
        else:
            print("\nFalha ao cadastrar aluguel.")
    
def registrarDevolucao():
    aluguel_id = input("ID do Aluguel: ")
    data_devolucao = input("Data de Devolução (AAAA-MM-DD): ")
    
    sql = "UPDATE aluguel SET data_devolucao = %s WHERE id_aluguel = %s;"
    params = (data_devolucao, aluguel_id)
    
    with ConexaoDB(db_config) as db:
        if db.manipular(sql, params):
            print("\nDevolução registrada com sucesso!")
        else:
            print("\nFalha ao registrar devolução.")

## MENU DO SISTEMA 
while True:
    print("\nBem-vindo ao Sistema de Biblioteca")
    print('''
    -------- Menu Principal --------
    
    1. Ver Livros
    2. Ver Clientes
    3. Ver Autores
    4. Ver Aluguéis
    5. Cadastrar Cliente
    6. Cadastrar Autor
    7. Cadastrar Aluguel
    8. Registrar Devolução
    9. Cadastrar Livro
    0. Sair
    ''')
    op = input("Escolha uma opção: ")
       
    if op == '1': verLivros()
    elif op == '2': verClientes()
    elif op == '3': verAutores()
    elif op == '4': verAlugueis()
    elif op == '5': cadastrarCliente()
    elif op == '6': cadastrarAutor()
    elif op == '7': cadastrarAluguel()
    elif op == '8': registrarDevolucao() 
    elif op == '9': cadastrarLivros()
    elif op == '0':
        print("Saindo...")
        break
    else:
        print("Opção inválida.")

    input("\nTECLE ENTER PARA CONTINUAR...")
    
    
    ## TESTE DE VERSIONAMENTO