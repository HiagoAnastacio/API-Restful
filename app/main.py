# Um dia será a parte Controller desta aplicação.
from fastapi import FastAPI
from model.database import Database
from model.basemodel import Serie, Autor, Motivo, Avaliacao, Categoria

 
app = FastAPI()
db = Database()

# Rotas para séries
@app.post("/series/")
def cadastrar_serie(serie: Serie):
    db.conectar()
    sql = "INSERT INTO serie (titulo_serie, descricao, ano_lancamento, categoria_id) VALUES (%s, %s, %s, %s)"
    db.executar_consultar(sql, (serie.titulo_serie, serie.descricao, serie.ano_lancamento, serie.categoria_id))
    db.desconectar()
    return {"saída": "Série cadastrada com sucesso"}
 
@app.get("/series/")
def listar_series():
    db.conectar()
    sql = "SELECT * FROM serie"
    series = db.executar_consultar(sql)
    db.desconectar()
    return series

@app.put("/update_serie/")
def atualizar_serie(serie_id: int, serie: Serie):
    db.conectar()
    sql = """
        UPDATE serie
        SET titulo_serie = %s, descricao = %s, ano_lancamento = %s, categoria_id = %s
        WHERE serie_id = %s
    """
    db.executar_consultar(sql, (serie.titulo_serie, serie.descricao, serie.ano_lancamento, serie.categoria_id, serie_id))
    db.desconectar()
    return {"saída": "Série atualizada com sucesso"}

@app.delete("/delete_serie/")
def deletar_serie(serie_id: int):
    db.conectar()
    sql = "DELETE FROM serie WHERE serie_id = %s"
    db.executar_consultar(sql, (serie_id,))
    db.desconectar()
    return {"saída": "Série deletada com sucesso"}
 
# Rotas para atores
@app.get("/atores/")
def listar_atores():
    db.conectar()
    sql = "SELECT * FROM autor"
    autores = db.executar_consultar(sql)
    db.desconectar()
    return autores

@app.post("/autor/")
def cadastrar_autor(autor: Autor):
    db.conectar()
    sql = "INSERT INTO autor (nome_autor) VALUES (%s)"
    db.executar_consultar(sql, (autor.nome,))
    db.desconectar()
    return {"saída": "Autor cadastrado com sucesso"}

# Rotas de associação entre informações
@app.get("/autor/{autor_id}/series/")
def listar_series_por_autor(autor_id: int):
    db.conectar()
    sql = """
        SELECT s.serie_id, s.titulo_serie, s.descricao, s.ano_lancamento
        FROM serie s
        JOIN autor_serie as ON s.serie_id = as.serie_id
        WHERE as.autor_id = %s
    """
    series = db.executar_consultar(sql, (autor_id,))
    db.desconectar()
    return series

@app.post("/autor/{autor_id}/series/{serie_id}")
def associar_autor_serie(autor_id: int, serie_id: int):
    db.conectar()   
    # Verifica se o autor e a série existem
    sql = "SELECT COUNT(*) FROM autor WHERE autor_id = %s"
    autor_count = db.executar_consultar(sql, (autor_id,))
    if autor_count[0]['COUNT(*)'] == 0:
        db.desconectar()
        return {"saída": "Autor não encontrado"}, 404
    sql = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
    serie_count = db.executar_consultar(sql, (serie_id,))
    if serie_count[0]['COUNT(*)'] == 0:
        db.desconectar()
        return {"saída": "Série não encontrada"}, 404
    # Se ambos existem, insere a associação
    sql = "INSERT INTO autor_serie (autor_id, serie_id) VALUES (%s, %s)"
    db.executar_consultar(sql, (autor_id, serie_id))
    db.desconectar()
    return {"saída": "Autor associado à série com sucesso"}, serie_id, autor_id

# Rotas para categorias
@app.get("/categorias/")
def listar_categorias():
    db.conectar()
    sql = "SELECT * FROM categoria"
    categorias = db.executar_consultar(sql)
    db.desconectar()
    return categorias

@app.post("/categorias/")
def adicionar_categoria(categoria: Categoria):
    db.conectar()
    sql = "INSERT INTO categoria (nome_categoria) VALUES (%s)"
    db.executar_consultar(sql, (categoria.nome,))
    db.desconectar()
    return {"saída": "Categoria adicionada com sucesso"}

 
# Rotas para motivos pessoais
@app.get("/motivos/")
def listar_motivos():
    db.conectar()
    sql = "SELECT * FROM motivo_assistir"
    motivos = db.executar_consultar(sql)
    db.desconectar()
    return motivos

@app.post("/motivos/")
def incluir_motivo(motivo: Motivo):
    db.conectar()
    sql = "INSERT INTO motivo_assistir (serie_id, motivo) VALUES (%s, %s)"
    db.executar_consultar(sql, (motivo.serie_id, motivo.motivo))
    db.desconectar()
    return {"saída": "Motivo incluído com sucesso"}
 
# Rotas para avaliações
@app.post("/avaliacoes/")
def avaliar_serie(avaliacao: Avaliacao):
    db.conectar()
    sql = "INSERT INTO avaliacao_serie (serie_id, nota, comentario) VALUES (%s, %s, %s)"
    db.executar_consultar(sql, (avaliacao.serie_id, avaliacao.nota, avaliacao.comentario))
    db.desconectar()
    return {"saída": "Avaliação registrada com sucesso"}
 
@app.get("/avaliacoes/")
def listar_avaliacoes():
    db.conectar()
    sql = "SELECT * FROM avaliacao_serie"
    avaliacoes = db.executar_consultar(sql)
    db.desconectar()
    return avaliacoes
 