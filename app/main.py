# Um dia será a parte Controller desta aplicação.
from fastapi import FastAPI, HTTPException
from typing import Type, Any
from model.database import Database
from model.basemodel import Serie, Autor, Motivo, Avaliacao, Categoria, BaseModel  # Importe BaseModel

app = FastAPI()
db = Database()

#FAZ FUNCIONAR O db.executar_consultar FUNCIONAR SEM UMA FUNÇÃO ANTERIOR O CHAMANDO
def executar_operacao_db(sql: str, params: tuple = None):
    db.conectar()
    db.executar_consultar(sql, params)
    db.desconectar()

def executar_consulta_db(sql: str, params: tuple = None):
    db.conectar()
    resultados = db.executar_consultar(sql, params)
    db.desconectar()
    return resultados

def rota_post(app: FastAPI, path: str, model: Type[BaseModel], nome_tabela: str):
    @app.post(path)
    def criar_item(item: model):
        campos = ", ".join(item.dict().keys())
        valores = ", ".join(["%s"] * len(item.dict()))
        sql = f"INSERT INTO {nome_tabela} ({campos}) VALUES ({valores})"
        executar_operacao_db(sql, tuple(item.dict().values()))
        return {"saída": f"{nome_tabela[:-1].capitalize()} cadastrado com sucesso"}
    return criar_item

def rota_get(app: FastAPI, path: str, nome_tabela: str):
    @app.get(path)
    def listar_itens():
        sql = f"SELECT * FROM {nome_tabela}"
        return executar_consulta_db(sql)
    return listar_itens

def rota_update(app: FastAPI, path: str, model: Type[BaseModel], nome_tabela: str, id_pk: str):
    @app.put(path)
    def atualizar_item(item_id: int, item: model):
        updates = ", ".join([f"{key} = %s" for key in item.dict().keys()])
        sql = f"UPDATE {nome_tabela} SET {updates} WHERE {id_pk} = %s"
        executar_operacao_db(sql, tuple(list(item.dict().values()) + [item_id]))
        return {"saída": f"{nome_tabela[:-1].capitalize()} atualizado com sucesso"}
    return atualizar_item

def rota_delete(app: FastAPI, path: str, nome_tabela: str, id_pk: str):
    @app.delete(path)
    def deletar_item(item_id: int):
        sql = f"DELETE FROM {nome_tabela} WHERE {id_pk} = %s"
        executar_operacao_db(sql, (item_id,))
        return {"saída": f"{nome_tabela[:-1].capitalize()} deletado com sucesso"}
    return deletar_item

# Aplicação das rotas genéricas
adicionar_serie = rota_post(app, "/series/", Serie, "serie")
listar_series = rota_get(app, "/series/", "serie")
atualizar_serie = rota_update(app, "/update_serie/{serie_id}", Serie, "serie", "serie_id")
deletar_serie = rota_delete(app, "/delete_serie/{serie_id}", "serie", "serie_id")

adicionar_autor = rota_post(app, "/autor/", Autor, "autor")
listar_atores = rota_get(app, "/atores/", "autor")
atualizar_autor = rota_update(app, "/update_autor/{autor_id}", Autor, "autor", "autor_id")
deletar_autor = rota_delete(app, "/delete_autor/{autor_id}", "autor", "autor_id")


adicionar_categoria = rota_post(app, "/categorias/", Categoria, "categoria")
listar_categorias = rota_get(app, "/categorias/", "categoria")
atualizar_categoria = rota_update(app, "/update_categoria/{categoria_id}", Categoria, "categoria", "categoria_id")
deletar_categoria = rota_delete(app, "/delete_categoria/{categoria_id}", "categoria", "categoria_id")

adicionar_motivo_pessoal = rota_post(app, "/motivos/", Motivo, "motivo_assistir")
listar_motivos = rota_get(app, "/motivos/", "motivo_assistir")
atualizar_motivo = rota_update(app, "/update_motivo/{motivo_id}", Motivo, "motivo_assistir", "motivo_id")
deletar_motivo = rota_delete(app, "/delete_motivo/{motivo_id}", "motivo_assistir", "motivo_id")

adcionar_atualizacao = rota_post(app, "/avaliacoes/", Avaliacao, "avaliacao_serie")
listar_avaliacoes = rota_get(app, "/avaliacoes/", "avaliacao_serie")
atualizar_avaliacao = rota_update(app, "/update_avaliacao/{avaliacao_id}", Avaliacao, "avaliacao_serie", "avaliacao_id")
deletar_avaliacao = rota_delete(app, "/delete_avaliacao/{avaliacao_id}", "avaliacao_serie", "avaliacao_id")

# Rotas de associação (estas são mais específicas e não se encaixam tão bem em funções genéricas)
@app.get("/autor/{autor_id}/series/")
def listar_serie_e_autor_relacionados(autor_id: int):
    sql = """
        SELECT s.serie_id, s.titulo_serie, s.descricao, s.ano_lancamento
        FROM serie s
        JOIN autor_serie as ON s.serie_id = as.serie_id
        WHERE as.autor_id = %s
    """
    return executar_consulta_db(sql, (autor_id,))

@app.post("/autor/{autor_id}/series/{serie_id}")
def associar_autor_serie(autor_id: int, serie_id: int):
    # Verifica se o autor e a série existem
    sql_autor = "SELECT COUNT(*) FROM autor WHERE autor_id = %s"
    autor_count = executar_consulta_db(sql_autor, (autor_id,))
    if autor_count[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    sql_serie = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
    serie_count = executar_consulta_db(sql_serie, (serie_id,))
    if serie_count[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=404, detail="Série não encontrada")
    # Se ambos existem, insere a associação
    sql_insert = "INSERT INTO autor_serie (autor_id, serie_id) VALUES (%s, %s)"
    executar_operacao_db(sql_insert, (autor_id, serie_id))
    return {"saída": "Autor associado à série com sucesso"}, serie_id, autor_id