from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
from models import Elenco
from models import Base
from erros import *

engine = create_engine("sqlite:///dados/banco.db")
Base.metadata.create_all(engine)


def adicionar_dados_json():
    with Session(engine) as session:
        if session.query(Elenco).count()>0:
            print("banco de dados ok")
        else:
            try:

                with open("dados/dados.json","r") as arquivo:
                    dados_json=json.load(arquivo)
                    lista_dados=list()
                    for c,n in enumerate(dados_json["elenco"]):    
                        dados=Elenco(nome=n["nome"],ator=n["ator"],status=n["status"],habilidades=n["habilidade"],upvote=n["upvote"])
                        lista_dados.append(dados)
                    session.add_all(lista_dados)
                    session.commit()
            except Exception as e:
                raise ErroNoBancoSql(e)
    
