from fastapi import FastAPI
from fastapi import HTTPException
from banco import adicionar_dados_json
from consulta import consulta
from erros import *

app=FastAPI()
buscar=consulta()

@app.get("/")
def home():
    return "ola mano"
   
@app.get("/elenco")
def elenco(status:str = None,habilidade:str=None,mais_votado:bool=False):
    try:
        dados=buscar.buscar_com_filtro(status_=status,habilidade_=habilidade,mais_votado_=mais_votado)
    except ValorVazio:
        raise HTTPException(status_code=404, detail="nenhum personagem encontrado com essas caracteristicas")
    except IndexError:
        raise HTTPException(status_code=404, detail="Erro inesperado ")
    return dados
@app.get("/elenco/{ator}")
def busca_ator(ator:str):
    try:
        
        dados_ator=buscar.buscar(modo="ator",nome=ator)
        
        return dados_ator
    except ErroValorMinimo:
        raise HTTPException(status_code=404, detail="Valor minimo de caracteres nao foram cumpridos")
    except ValorVazio():
        raise HTTPException(status_code=404, detail="ator nao enconstrado")
@app.get("/personagem/{personagem}")
def buscar_personagem(personagem:str):
    try:
        dados_personagem=buscar.buscar(modo="personagem",nome=personagem)
       
        return dados_personagem
    except ErroValorMinimo:
        raise HTTPException(status_code=404, detail="Valor minimo de caracteres nao foram cumpridos")
    except ValorVazio():
        raise HTTPException(status_code=404, detail="personagem nao enconstrado")
@app.post("/votar/{personagem}")
def upvote(personagem):
    try:
        voto=buscar.atualizar_voto(personagem)
        return "sucesso"
    except ErroNenhumResultado:
         raise HTTPException(status_code=404, detail="personagem não encontrado")
    except ValorVazio:
        raise  HTTPException(status_code=404, detail="personagem não encontrado")
#uvicorn main:app --reload
