from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
from models import User
from models import Base

engine = create_engine("sqlite:///dados/banco.db")
Base.metadata.create_all(engine)

class banco():
    def __init__(self):  
        pass
    def adicionar_dados_json(self):
        with Session(engine) as session:
            if session.query(User).count()>0:
                print("banco de dados ok")
            else:
                try:

                    with open("dados/dados.json","r") as arquivo:
                        dados_json=json.load(arquivo)
                        lista_dados=list()
                        for c,n in enumerate(dados_json["elenco"]):    
                            dados=User(nome=n["nome"],ator=n["ator"],status=n["status"],habilidades=n["habilidade"],upvote=n["upvote"])
                            lista_dados.append(dados)
                        session.add_all(lista_dados)
                        session.commit()
                except Exception as e:
                    print(f"erro no banco.py {e}")
    

