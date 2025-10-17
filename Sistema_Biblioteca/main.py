import mysql.connector
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

## FUNÇÕES DO SISTEMA
def verLivros():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM livros;")
        livros = cursor.fetchall()
        
        if livros:
            print("\nLista de Livros:")
            print()
            for livro in livros:
                print(f"ID: {livro[0]} | Título: {livro[1]} | Ano: {livro[2]}")
            print()
        else:
            print("Nenhum livro encontrado.")
        
    except mysql.connector.Error as erro:
        print(f"Erro ao buscar livros: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cadastrarLivros():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        titulo = input("Título do Livro: ")
        ano = input("Ano de Publicação: ")
        autor_id = input("ID do Autor: ")
        
        cursor.execute("INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES (%s, %s, %s);", 
                       (titulo, ano, autor_id))
        conn.commit()
        
        print()
        print("Livro cadastrado com sucesso!")
        print()
        
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar livro: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def verClientes():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clientes;")
        clientes = cursor.fetchall()
        
        if clientes:
            print("\nLista de Clientes:")
            print()
            for cliente in clientes:
                print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | CPF: {cliente[3]}")
            print()
        else:
            print("Nenhum cliente encontrado.")
        
    except mysql.connector.Error as erro:
        print(f"Erro ao buscar clientes: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
def verAutores():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM autores;")
        autores = cursor.fetchall()
        
        if autores:
            print("\nLista de Autores:")
            print()
            for autor in autores:
                print(f"ID: {autor[0]} | Nome: {autor[1]}")
            print()
        else:
            print("Nenhum autor encontrado.")
        
    except mysql.connector.Error as erro:
        print(f"Erro ao buscar autores: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def verAlugueis():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT a.id_aluguel, l.titulo_livro, c.nome_cliente, a.data_aluguel, a.data_devolucao
        FROM aluguel a
        JOIN livros l ON a.livro_id = l.id_livro
        JOIN clientes c ON a.cliente_id = c.id_cliente;
        ''')
        alugueis = cursor.fetchall()
        
        if alugueis:
            print("\nLista de Aluguéis:")
            print()
            for aluguel in alugueis:
                print(f"ID: {aluguel[0]} | Livro: {aluguel[1]} | Cliente: {aluguel[2]} | Data Aluguel: {aluguel[3]} | Data Devolução: {aluguel[4]}")
            print()
        else:
            print("Nenhum aluguel encontrado.")
        
    except mysql.connector.Error as erro:
        print(f"Erro ao buscar aluguéis: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cadastrarCliente():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        nome = input("Nome do Cliente: ")
        email = input("Email do Cliente (deixe em branco se não tiver): ")
        cpf = input("CPF do Cliente (11 dígitos): ")
        endereco = input("Endereço do Cliente: ")
        telefone = input("Telefone do Cliente (11 dígitos): ")
        
        email = email if email else None  # Permitir email nulo
        
        cursor.execute('''
        INSERT INTO clientes (nome_cliente, email, cpf_cliente, endereco_cliente, telefone_cliente)
        VALUES (%s, %s, %s, %s, %s);
        ''', (nome, email, cpf, endereco, telefone))
        conn.commit()
        
        print()
        print("Cliente cadastrado com sucesso!")
        print()
        
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar cliente: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cadastrarAutor():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        nome = input("Nome do Autor: ")
        
        cursor.execute("INSERT INTO autores (nome_autor) VALUES (%s);", (nome,))
        conn.commit()
        
        print()
        print("Autor cadastrado com sucesso!")
        print()
        
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar autor: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def cadastrarAluguel():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        livro_id = input("ID do Livro: ")
        cliente_id = input("ID do Cliente: ")
        data_aluguel = input("Data de Aluguel (YYYY-MM-DD): ")
        
        cursor.execute('''
        INSERT INTO aluguel (livro_id, cliente_id, data_aluguel)
        VALUES (%s, %s, %s);
        ''', (livro_id, cliente_id, data_aluguel))
        conn.commit()
        
        print()
        print("Aluguel cadastrado com sucesso!")
        print()
        
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar aluguel: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
def registrarDevolucao():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        aluguel_id = input("ID do Aluguel: ")
        data_devolucao = input("Data de Devolução (YYYY-MM-DD): ")
        
        cursor.execute('''
        UPDATE aluguel
        SET data_devolucao = %s
        WHERE id_aluguel = %s;
        ''', (data_devolucao, aluguel_id))
        conn.commit()
        
        print()
        print("Devolução registrada com sucesso!")
        print()
        
    except mysql.connector.Error as erro:
        print(f"Erro ao registrar devolução: {erro}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

## MENU DO SISTEMA
while True:
    print()
    print("Bem-vindo ao Sistema de Biblioteca")
    print()
    
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
       
    if op == '1':
        verLivros()
    elif op == '2':
        verClientes()
    elif op == '3':
        verAutores()
    elif op == '4':
        verAlugueis()
    elif op == '5':
        cadastrarCliente()
    elif op == '6':
        cadastrarAutor()
    elif op == '7':
        cadastrarAluguel()
    elif op == '8':
        registrarDevolucao() 
    elif op == '9':
        cadastrarLivros()
    elif op == '0':
        print("Saindo...")
        break

    input("TECLE ENTER PARA CONTINUAR...")

