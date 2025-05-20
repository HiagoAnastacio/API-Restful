# Este é o Controller desta aplicação.
from fastapi import FastAPI, HTTPException, status
from typing import Type, List
from model.database import Database
from model.basemodel import BaseModel
from routes import genericas, serie_autor

# Instanciamento do FastAPI e do banco de dados. 
app = FastAPI()
db = Database()

# Função que utiliza a lógica elaborada no database.py para executar operações no banco de dados.
def executar_operacao_db(sql: str, params: tuple = None):
    try:
        db.conectar()
        resultado = db.executar_comando(sql, params)
        db.desconectar()
        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=500, detail=str(e))

# Função que busca as tabelas no banco de dados e retorna uma lista com os nomes das tabelas. 
def achar_listar_tabelas(tabelas: List[str]):
    sql = "SELECT `table_name` FROM information_schema.tables WHERE table_schema = 'mustwatch';"
    resultado = executar_operacao_db(sql)
    tabelas = [linha['TABLE_NAME'] for linha in resultado]
    return tabelas

# Função que cria as rotas para cada tabela do banco de dados, utilizando os métodos HTTP apropriados (GET, POST, UPDATE, DELETE).
def criar_rota_por_tabela(nome_tabela: str, tabelas: List[str], model: Type[BaseModel]):
    for nome_tabela in tabelas:
        genericas.rota_get(app, f"/{nome_tabela}", nome_tabela)
        genericas.rota_post(app, f"/{nome_tabela}", model, nome_tabela)
        genericas.rota_update(app, f"/{nome_tabela}/{{item_id}}", model, nome_tabela, "id")
        genericas.rota_delete(app, f"/{nome_tabela}/{{item_id}}", nome_tabela, "id")

#Instanciamento das rotas associativas
serie_autor.listar_serie_e_autor_relacionados
serie_autor.associar_autor_serie
serie_autor.atualizar_associar_autor_serie
serie_autor.deletar_associacao_autor_serie

# Instanciamento da criação das demias rotas
tabelas = achar_listar_tabelas([])
criar_rota_por_tabela("", tabelas, BaseModel)
 