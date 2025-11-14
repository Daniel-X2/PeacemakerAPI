
from sqlalchemy import String
from sqlalchemy import INTEGER
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import create_engine,update
from sqlalchemy.orm import Session
import json
import os
from sqlalchemy import select


class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__="user_account"

    id:Mapped[int]=mapped_column(primary_key=True)
    nome:Mapped[str]=mapped_column(String(30))
    ator:Mapped[str]=mapped_column(String(30))
    status:Mapped[str]=mapped_column(String(10))
    habilidades:Mapped[list]=mapped_column(JSON)
    upvote:Mapped[int]=mapped_column(INTEGER)


class banco():
    def __init__(self):
        self.engine = create_engine("sqlite:///dados/banco.db", echo=True)
        Base.metadata.create_all(self.engine)
        self.adicionar_dados_json()
        self.buscar_elenco("morto","Matador")
    def adicionar_dados_json(self):
        with Session(self.engine) as session:
            if session.query(User).count()>0:
                print("banco de dados ok")
            else:
                with open("dados/dados.json","r") as arquivo:
                    teste=json.load(arquivo)
                    for c,n in enumerate(teste["elenco"]):    
                        outro=User(nome=n["nome"],ator=n["ator"],status=n["status"],habilidades=n["habilidade"],upvote=n["upvote"])
                        session.add(outro)
                        session.commit()
    
    def buscar_elenco(self,status=None,habilidade=None,mais_votado=False):
        with Session(self.engine) as session:
            parametros=list()
            if(status==None and habilidade==None and mais_votado==False):
                elenco=session.query(User.nome,User.ator,User.status,
                    User.habilidades,User.upvote).all()
            else:
                if(status!=None and habilidade!=None and mais_votado!= False):
                    elenco=session.query(User.nome,User.ator,User.status,
                    User.habilidades,User.upvote).filter(User.status==status,User.habilidades==habilidade).first()
                else:
                    if(status!=None):
                        parametros.append(User.status == status)
                    
                    if(habilidade!=None):
                        parametros.append(User.habilidades.ilike(f"%{habilidade}%") )
                    if(mais_votado==True):
                        parametros.append(User.status )
                elenco=session.query(User.nome,User.ator,User.status,
                    User.habilidades,User.upvote).filter(parametros.pop(),parametros.pop()).all()
                
            lista_de_dict=list()
            dicionario=dict()
            try:
                for c in range(0,len(elenco)):
                    dicionario={"nome":elenco[c][0],"ator":elenco[c][1],"status":elenco[c][2],
                    "habilidade":elenco[c][3],"upvote":elenco[c][4]}
                    lista_de_dict.append(dicionario)
                return lista_de_dict
            except IndexError:
                for c in range(0,len(elenco[0])):
                    dicionario={"nome":elenco[c][0],"ator":elenco[c][1],"status":elenco[c][2],
                    "habilidade":elenco[c][3],"upvote":elenco[c][4]}
                    lista_de_dict.append(dicionario)
                return lista_de_dict
    def atualizar_voto(self,personagem):
         with Session(self.engine) as session:
            ##
            #esse User.ator.ilike ele nao faz diferenciaçao entre maiusculo ou minusculo 
            #  se tiver  john como parametro e aparecer jjjjohnnn ele vai pegar como se fosse 
            #john
            #  ##
            n1=session.query(User.nome).filter(User.nome.ilike(f"%{personagem}%"))
            try:
                n1[0]
            except IndexError:
                return 1   
            try:
                contagem=session.query(User.upvote).filter(User.nome.ilike(f"%{personagem}%"))
                atualizacao=update(User).filter(User.nome.ilike(f"%{personagem}%")).values(upvote=contagem[0][0]+1)   
                session.execute(atualizacao)
                session.commit()   
            except:
                return 2
            return 0
    
    def buscar(self,atorr,personagem=None):
        with Session(self.engine) as session:
            if(personagem==None):
                
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.ator.ilike(f"%{atorr}%"))
                return {"nome":dados[0][0],"ator":dados[0][1],"status":dados[0][2],"habilidade":dados[0][3],"upvote":dados[0][4]}
            else:
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.nome.ilike(f"%{personagem}%"))
                return {"nome":dados[0][0],"ator":dados[0][1],"status":dados[0][2],"habilidade":dados[0][3],"upvote":dados[0][4]}
banco()