import mysql.connector

class ConexaoDB:
    def __init__(self, config):
        """ Salva a configuração do banco ao criar o objeto. """
        self._config = config
        self._conn = None
        self._cursor = None

    def __enter__(self):
        """ Abre a conexão ao iniciar o bloco 'with'. """
        try:
            self._conn = mysql.connector.connect(**self._config)
            # dictionary=True retorna resultados como dicionários (ex: {'id': 1, 'nome': 'Diego'})
            # É muito mais fácil de trabalhar do que com índices (ex: linha[0], linha[1])
            self._cursor = self._conn.cursor(dictionary=True)
            return self
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise # Lança o erro para interromper a execução no 'with'

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Fecha a conexão ao finalizar o bloco 'with', mesmo se ocorrer um erro. """
        if self._conn and self._conn.is_connected():
            self._cursor.close()
            self._conn.close()

    def consultar(self, sql, params=None):
        """ Executa uma consulta SELECT e retorna todos os resultados. """
        try:
            self._cursor.execute(sql, params or ())
            return self._cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Erro ao executar consulta: {e}")
            return None # Retorna None em caso de falha

    def manipular(self, sql, params=None):
        """ Executa INSERT, UPDATE, DELETE. """
        try:
            self._cursor.execute(sql, params or ())
            self._conn.commit()
            return True # Retorna True em caso de sucesso
        except mysql.connector.Error as e:
            print(f"Erro ao manipular dados: {e}")
            self._conn.rollback() # Desfaz a operação em caso de erro
            return False # Retorna False em caso de falha