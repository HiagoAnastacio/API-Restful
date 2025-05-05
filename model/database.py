import mysql.connector as mc # Importando a biblioteca do conector do MySQL
from mysql.connector import Error, MySQLConnection # Importando a classe Error para tratar as mensagens de erro do código
from dotenv import load_dotenv # Importando a função load_dotenv
from os import getenv
from typing import Optional, Any, Tuple, List

class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.host: str = getenv('DB_HOST')
        self.username: str = getenv('DB_USER')
        self.password: str = getenv('DB_PSWD')
        self.database: str = getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None # Inicialização da conexão
        self.cursor: Optional[List[dict]] = None # Inicialização do cursor

    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password = self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print('Conexão ao banco de dados realizada com sucesso!')
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('Conexão com o banco de dados encerrada com sucesso!')

    def executar_consultar(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[dict]]:
        """Executa uma instrução no banco de dados, determinando automaticamente se é uma consulta ou uma modificação."""
        if self.connection is None or self.cursor is None:
            print('Conexão ao banco de dados não estabelecida!')
            return None
        try:
            # Executa o comando SQL
            self.cursor.execute(sql, params)

            # Verifica se o comando é uma consulta (SELECT)
            if sql.strip().lower().startswith("select"):
                resultado = self.cursor.fetchall()
                return resultado
            else:
                # Caso contrário, é uma modificação no banco de dados
                self.connection.commit()
                return None
        except Error as e:
            print(f'Erro de execução: {e}')
            return None
        

db = Database() # Instância da classe Database
db.conectar() # Conexão com o banco de dados