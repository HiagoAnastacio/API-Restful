# Junto ao database.py, isso é o Model (onde a lógica do banco de dados ocorre e no caso deste arquivo a adaptação para o banco de dados, por meio da validação de dados, ou seja, ele permite criar classes que representam os dados esperados em uma aplicação, garantindo que os dados recebidos ou enviados estejam no formato correto.) desta aplicação.
from pydantic import BaseModel
from typing import Optional
from model.database import Database

db = Database()

# Modelos Pydantic
class Serie(BaseModel):
    titulo_serie: str
    descricao: Optional[str]
    ano_lancamento: Optional[int]
    categoria_id: int
 
class Autor(BaseModel):
    nome: str
 
class Motivo(BaseModel):
    serie_id: int
    motivo: str
 
class Avaliacao(BaseModel):
    serie_id: int
    nota: int
    comentario: Optional[str]
 
class Categoria(BaseModel):
    nome: str

class AutorSerie(BaseModel):
    autor_id: int
    serie_id: int 
