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
 
# Rotas para atores
@app.post("/autores/")
def cadastrar_autor(autor: Autor):
    db.conectar()
    sql = "INSERT INTO ator (nome) VALUES (%s)"
    db.executar_consultar(sql, (autor.nome,))
    db.desconectar()
    return {"saída": "Autor cadastrado com sucesso"}
 
@app.post("/autores/{autor_id}/series/{serie_id}")
def associar_ator_serie(autor_id: int, serie_id: int, personagem: str):
    db.conectar()
    sql = "INSERT INTO autor_serie (autor_id, serie_id, personagem) VALUES (%s, %s, %s)"
    db.executar_consultar(sql, (autor_id, serie_id, personagem))
    db.desconectar()
    return {"saída": "Autor associado à série com sucesso"}
 
# Rotas para categorias
@app.get("/categorias/")
def listar_categorias():
    db.conectar()
    sql = "SELECT * FROM categoria"
    categorias = db.executar_consultar(sql)
    db.desconectar()
    return categorias
 
# Rotas para motivos pessoais
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
 
@app.post("/categorias/")
def adicionar_categoria(categoria: Categoria):
    db.conectar()
    sql = "INSERT INTO categoria (nome) VALUES (%s)"
    db.executar_consultar(sql, (categoria.nome,))
    db.desconectar()
    return {"saída": "Categoria adicionada com sucesso"}
 