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

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    ##cursor.execute("SELECT VERSION();")
    ##version = cursor.fetchone()
    
    cursor.execute("DROP TABLE IF EXISTS aluguel;")
    cursor.execute("DROP TABLE IF EXISTS clientes;")
    cursor.execute("DROP TABLE IF EXISTS livros;")
    cursor.execute("DROP TABLE IF EXISTS autores;")
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS autores (
        id_autor INT AUTO_INCREMENT PRIMARY KEY,
        nome_autor VARCHAR(100) NOT NULL
    );
    ''')
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id_livro INT AUTO_INCREMENT PRIMARY KEY,
        titulo_livro VARCHAR(100) NOT NULL,
        ano_publicacao INT,
        autor_id INT,
        CONSTRAINT fk_livro_autor FOREIGN KEY (autor_id) REFERENCES autores(id_autor)
    );
    ''')
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NULL,
    cpf_cliente VARCHAR(11) UNIQUE,
    endereco_cliente VARCHAR(255),
    telefone_cliente VARCHAR(11),
    data_nascimento DATE,
    CONSTRAINT chk_email_formato CHECK (email IS NULL OR email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
    );
    ''')
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS aluguel (
        id_aluguel INT AUTO_INCREMENT PRIMARY KEY,
        livro_id INT,
        cliente_id INT,
        data_aluguel DATE,
        data_devolucao DATE,
        CONSTRAINT fk_aluguel_livro FOREIGN KEY (livro_id) REFERENCES livros(id_livro),
        CONSTRAINT fk_aluguel_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente)
    );
    ''')
    conn.commit()

    cursor.execute('''
    INSERT INTO autores (nome_autor) VALUES
    ('J.K. Rowling'), ('George R.R. Martin'), ('J.R.R. Tolkien');
    ''')
    conn.commit()

    cursor.execute('''
    INSERT INTO livros (titulo_livro, ano_publicacao, autor_id) VALUES
    ('Harry Potter e a Pedra Filosofal', 1997, 1),
    ('A Guerra dos Tronos', 1996, 2),
    ('O Senhor dos Anéis: A Sociedade do Anel', 1954, 3),
    ('A Fúria dos Reis', 1998, 2),
    ('O Senhor dos Anéis: As Duas Torres', 1954, 3);
    ''')
    conn.commit()

    cursor.execute('''
    INSERT INTO clientes (nome_cliente, email, cpf_cliente, endereco_cliente, telefone_cliente, data_nascimento) VALUES
    ('Cristiana santos', 'cristiana.s@email.com', '12345678901', 'Rua A, 123', '85987654321', '1990-05-15'),
    ('Diego simiao', 'diego.simiao@email.com', '10987654321', 'Avenida B, 456', '85912345678', '1991-08-22');
    ''')
    conn.commit()
    
    cursor.execute('''
    INSERT INTO aluguel (livro_id, cliente_id, data_aluguel) VALUES
    (1, 1, '2025-10-10'),
    (2, 2, '2025-10-12'),
    (4, 1, '2025-10-14');
    ''')
    conn.commit()
    
    cursor.execute('''
    UPDATE aluguel
    SET data_devolucao = '2025-10-14'
    WHERE id_aluguel = 1;
    ''')
    conn.commit()

    cursor.close()
    conn.close()

    print("Banco de dados configurado com sucesso!")
except mysql.connector.Error as erro:
    print(f"B.O VIU! Erro de SQL! {erro}")
except Exception as erro:
    print(f"B.O VIU! Erro inesperado! {erro}")