from fastapi import FastAPI, HTTPException, status
from app.main import executar_operacao_db 
from fastapi import Query

app = FastAPI()

# Rota GET
@app.get("/autor/{autor_id}/series/", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Séries encontradas para o autor"},
    status.HTTP_404_NOT_FOUND: {"description": "Nenhuma série encontrada para o autor especificado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def listar_serie_e_autor_relacionados(autor_id: int,  serie_id: int):
    """
    Lista todas as séries associadas a um autor específico.
    """
    sql = """
        SELECT s.serie_id, s.titulo_serie, s.descricao, s.ano_lancamento
        FROM serie s
        JOIN autor_serie AS `as` ON s.serie_id = `as`.serie_id -- Use alias para evitar conflito com 'as' keyword
        WHERE `as`.autor_id = %s
    """
    resultado = executar_operacao_db(sql, (autor_id, serie_id))
    
    if resultado:
        return resultado
    # Se não houver resultado, levanta 404 (Nenhum item encontrado)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nenhuma série encontrada para o autor ID {autor_id}.")

#Rota POST
@app.post("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre autor e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "Autor ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def associar_autor_serie(autor_id: int, serie_id: int):
    """
    Associa uma série a um autor.
    """
    # 1. Verifica se o autor existe
    sql_autor = "SELECT COUNT(*) FROM autor WHERE autor_id = %s"
    autor_count_result = executar_operacao_db(sql_autor, (autor_id,))
    # Adicionado 'not autor_count_result' para lidar com um possível None ou lista vazia se a query falhar
    if not autor_count_result or autor_count_result[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Autor com ID {autor_id} não encontrado.")
    
    # 2. Verifica se a série existe
    sql_serie = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
    sql_serie_exis = executar_operacao_db(sql_serie, (serie_id,))
    if not sql_serie_exis or sql_serie_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Série com ID {serie_id} não encontrada.")
    
    # 3. Verifica se a associação já existe para evitar duplicatas
    sql_exis_associacao = "SELECT COUNT(*) FROM autor_serie WHERE autor_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (autor_id, serie_id))
    if resultado_associacao_exis and resultado_associacao_exis[0]['COUNT(*)'] > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Associação entre este autor e série já existe.") # 409 Conflict para duplicidade
    
    # 4. Se tudo OK, insere a associação
    sql_insert = "INSERT INTO autor_serie (autor_id, serie_id) VALUES (%s, %s)"
    executar_operacao_db(sql_insert, (autor_id, serie_id)) 

    # Retorno conforme suas rotas genéricas para consistência
    return {"saída": f"Associação entre autor ID {autor_id} e série ID {serie_id} criada com sucesso!"}

#Rota UPDATE
@app.update("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_201_CREATED: {"description": "Associação entre autor e série criada com sucesso"},
    status.HTTP_400_BAD_REQUEST: {"description": "Associação já existe ou dados inválidos"},
    status.HTTP_404_NOT_FOUND: {"description": "Autor ou série não encontrado"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def atualizar_associar_autor_serie(autor_id: int, serie_id: int):
    """
    Atualiza a associação entre autor e série (exemplo: trocar a série associada a um autor).
    Para este exemplo, vamos supor que queremos atualizar a série associada a um autor para uma nova série.
    """
    # Verifica se a associação existe
    sql_exis_associacao = "SELECT COUNT(*) FROM autor_serie WHERE autor_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (autor_id, serie_id))
    if not resultado_associacao_exis or resultado_associacao_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação entre este autor e série não existe.")

    # Exemplo: atualizar para uma nova série (novo_serie_id passado como query param ou body, aqui usaremos query param)
    # Para simplificação, vamos supor que o novo_serie_id é passado como query param
    def inner_update(novo_serie_id: int = Query(..., description="Novo ID da série para atualizar a associação")):
        # Verifica se a nova série existe
        sql_serie = "SELECT COUNT(*) FROM serie WHERE serie_id = %s"
        sql_serie_exis = executar_operacao_db(sql_serie, (novo_serie_id,))
        if not sql_serie_exis or sql_serie_exis[0]['COUNT(*)'] == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Série com ID {novo_serie_id} não encontrada.")

        # Atualiza a associação
        sql_update = "UPDATE autor_serie SET serie_id = %s WHERE autor_id = %s AND serie_id = %s"
        executar_operacao_db(sql_update, (novo_serie_id, autor_id, serie_id))
        return {"saída": f"Associação do autor ID {autor_id} atualizada para série ID {novo_serie_id} com sucesso!"}
    return inner_update

#Rota DELETE
@app.delete("/autor/{autor_id}/series/{serie_id}", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {"description": "Associação entre autor e série removida com sucesso"},
    status.HTTP_404_NOT_FOUND: {"description": "Associação não encontrada"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Erro interno do servidor"}
})
def deletar_associacao_autor_serie(autor_id: int, serie_id: int):
    """
    Remove a associação entre um autor e uma série.
    """
    # Verifica se a associação existe
    sql_exis_associacao = "SELECT COUNT(*) FROM autor_serie WHERE autor_id = %s AND serie_id = %s"
    resultado_associacao_exis = executar_operacao_db(sql_exis_associacao, (autor_id, serie_id))
    if not resultado_associacao_exis or resultado_associacao_exis[0]['COUNT(*)'] == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação entre este autor e série não existe.")

    # Remove a associação
    sql_delete = "DELETE FROM autor_serie WHERE autor_id = %s AND serie_id = %s"
    executar_operacao_db(sql_delete, (autor_id, serie_id))
    return {"saída": f"Associação entre autor ID {autor_id} e série ID {serie_id} removida com sucesso!"}
