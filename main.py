from fastapi import FastAPI
from fastapi import HTTPException

from banco import banco
from consulta import consulta


app=FastAPI()
db=banco()
busca=consulta()

@app.get("/")
def home():
    return "ola mano"
   
@app.get("/elenco")
def elenco(status:str = None,habilidade:str=None,mais_votado:bool=False):
    n1=busca.buscar_no_elenco(status_=status,habilidade_=habilidade,mais_votado_=mais_votado)
    print(n1)
    return n1
@app.get("/elenco/{ator}")
def busca_ator(ator:str):
    try:
        dados_ator=busca.buscar_no_elenco(ator_=ator)
        
        if (dados_ator):
           
            return dados_ator
        else:
            raise HTTPException(status_code=404, detail="Ator não encontrado")
    except Exception as e:
        print(f"erro no main.py {e}") 
        raise HTTPException(status_code=404, detail="ator nao enconstrado")
@app.get("/personagem/{personagem}")
def buscar_personagem(personagem:str):
    try:
        dados_personagem=busca.buscar_no_elenco(personagem_=personagem)
        if (dados_personagem):
            return dados_personagem
        else:
            raise HTTPException(status_code=404, detail="personagem não encontrado")
    except Exception as e:
        print(f"erro main.py {e}")
        raise HTTPException(status_code=404, detail="personagem nao encontrado")
@app.post("/votar/{personagem}")
def upvote(personagem):
    voto=busca.atualizar_voto(personagem)
    if voto==0:
        return "adicionado com sucesso"
    elif voto==1:
        raise HTTPException(status_code=404, detail="personagem não encontrado")
    else:
        raise HTTPException(status_code=400, detail="problema no banco de dados")
#uvicorn main:app --reload