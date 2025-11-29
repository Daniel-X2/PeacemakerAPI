from fastapi import FastAPI
from fastapi import HTTPException
from src.Erros_personalizado.erros import *
from src.service.main_service import ElencoService
from dados.banco import adicionar_dados_json
from contextlib import asynccontextmanager
from pydantic import constr



@asynccontextmanager
async def lifespan(app: FastAPI):
    adicionar_dados_json()  # executa só na inicialização da API
    yield

app = FastAPI(lifespan=lifespan)
service = ElencoService()

@app.get("/")
def home() -> dict:
    """
    Endpoint de teste da API.
    
    Returns:
        str: Mensagem de boas-vindas.
    """
    return {"message": "API Pacificador",
        "version": "1.0",
        "docs": "/docs"}

@app.get("/elenco")
def elenco() -> list:
    """
    Retorna todo o elenco cadastrado no banco de dados.
    
    Returns:
        list: Lista com todos os atores e personagens.
        
    Raises:
        HTTPException: Erro 204 se o elenco estiver vazio.
    """
    try:
        return service.retornar_elenco()
    except ValorVazio:
        raise HTTPException(status_code=204,
                            detail="O valor retornado está vazio")

@app.get("/busca/")
def busca_com_filtro(vivo: bool = True, habilidade: str = None, mais_votado: bool = False) :
    """
    Busca personagens com filtros personalizados.
    
    Args:
        vivo (bool): Filtrar por personagens vivos. Padrão: True.
        habilidade (str): Filtrar por habilidade específica. Padrão: None.
        mais_votado (bool): Ordenar pelos mais votados. Padrão: False.
        
    Returns:
        list: Lista de personagens que correspondem aos critérios.
        
    Raises:
        HTTPException: Erro 404 se nenhum resultado for encontrado.
        HTTPException: Erro 422 se houver erro de validação.
        HTTPException: Erro 400 se nenhum parâmetro for selecionado.
    """
    try:
        dados = service.buscar_com_filtro(vivo=vivo,
                                        habilidade=habilidade,
                                        mais_votado=mais_votado)
    except ErroNenhumResultado:
        raise HTTPException(
                            status_code=404,
                            detail="nenhum personagem encontrado com essas características")
    except ErroValidacao:
        raise HTTPException(
                            status_code=422, 
                            detail="Erro ao validar os dados inseridos")
    except ErroSemParametros:
        raise HTTPException(
                            status_code=400, 
                            detail="Nenhum parâmetro selecionado")
    except ErroValorMinimo:
        raise HTTPException(
                            status_code=422, 
                            detail="o parâmetro habilidade não tem o valor mínimo")
    return dados

@app.get("/elenco/{ator}")
def busca_ator(ator:str) :
    """
    Busca informações completas de um ator específico.
    
    Args:
        ator (str): Nome do ator a buscar (mínimo 3 caracteres).
        
    Returns:
        dict: Informações completas do ator encontrado.
        
    Raises:
        HTTPException: Erro 422 se o nome tiver menos de 3 caracteres.
        HTTPException: Erro 404 se o ator não for encontrado.
    """
    try:
        if(len(ator.strip())<3):
            raise ErroValorMinimo
        dados_ator = service.buscar_no_elenco(nome=ator, modo="ator")

        return dados_ator
    except ErroValorMinimo:
        raise HTTPException(status_code=422,
                            detail="Valor mínimo de caracteres não foi cumprido")
    except ErroValidacao:
        raise HTTPException(status_code=422,
                            detail="erro na validação dos dados inseridos")
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="ator não encontrado")

@app.get("/personagem/{personagem}")
def buscar_personagem(personagem: str) -> dict:
    """
    Busca informações completas de um personagem específico.
    
    Args:
        personagem (str): Nome do personagem a buscar (mínimo 3 caracteres).
        
    Returns:
        dict: Informações completas do personagem encontrado.
        
    Raises:
        HTTPException: Erro 422 se o nome tiver menos de 3 caracteres.
        HTTPException: Erro 404 se o personagem não for encontrado.
    """
    try:
        if(len(personagem.strip())<3):
            raise ErroValorMinimo
        dados_personagem = service.buscar_no_elenco(nome=personagem, modo="personagem")
        
        return dados_personagem
    except ErroValorMinimo:
        raise HTTPException(status_code=422,
                            detail="Valor mínimo de caracteres não foi cumprido")
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="personagem não encontrado")
    except ErroValidacao:
        raise HTTPException(status_code=422,
                            detail="erro na validação dos dados inseridos")

@app.post("/votar/{personagem}")
def upvote(personagem: str) -> dict:
    """
    Registra um voto para um personagem específico.
    
    Args:
        personagem (str): Nome do personagem a votar (mínimo 3 caracteres).
        
    Returns:
        dict: Status da operação.
        
    Raises:
        HTTPException: Erro 422 se o nome tiver menos de 3 caracteres.
        HTTPException: Erro 404 se o personagem não for encontrado.
    """
    try:
        if(len(personagem.strip())<3):
            raise ErroValorMinimo
        result=service.votar(personagem)
        if(result==1):
            return {"status": "sucesso"}
        else:
            return {"status": "falha"}
    except ErroNenhumResultado:
        raise HTTPException(status_code=404,
                            detail="personagem não encontrado")
    except ErroValorMinimo:
        raise HTTPException(status_code=422,
                            detail="o valor mínimo de caracteres não foi alcançado")

@app.get("/ranking/")
def ranking(top: int = 3) -> dict:
    """
    Retorna o ranking dos personagens mais votados.
    
    Args:
        top (int): Quantidade de posições no ranking. Padrão: 3.
        
    Returns:
        dict: Ranking com os personagens mais votados.
        
    Raises:
        HTTPException: Erro 422 se o valor de 'top' for menor ou igual a 0.
        HTTPException: Erro 204 se o ranking estiver vazio.
    """
    try:
        if(top<=0):
            raise HTTPException(status_code=422,
                                detail="O parâmetro 'top' deve ser positivo")
        return service.ranking(top)
    except ValorVazio:
        raise HTTPException(status_code=204,
                            detail="o valor retornado está vazio")
    

@app.get("/stats")
def estatisticas() -> dict:
    """
    Retorna estatísticas gerais do elenco e personagens.
    
    Returns:
        dict: Dicionário com estatísticas (total de personagens, vivos, etc).
        
    Raises:
        HTTPException: Erro 204 se as estatísticas estiverem vazias.
    """
    try:
        return service.stats()
    except ValorVazio:
         raise HTTPException(status_code=204,
                            detail="O valor retornado está vazio")

# uvicorn main:app --reload
