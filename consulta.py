from sqlalchemy import update
from sqlalchemy.orm import Session
from banco import engine
from models import User

###
# mano vou criar classes de exceçoes pra facilitar meu uso 
# e facilitar o diagnostico de erro
# ##
class consulta():
    def __init__(self):
        pass
    
    def buscar_com_filtro(self,habilidade_:str=None,status_=None,mais_votado_=False):
        with Session(engine) as session:
            # #
            # aqui faz a filtragem da pesquisa
            # #
            busca=session.query(User.nome,User.ator,User.status,
            User.habilidades,User.upvote)

            if(status_==None and habilidade_==None and mais_votado_==False):
                #aqui serve principalmente pra listar todos no elenco
                return self.loop_busca(busca.all(),False)
            if(status_!=None):
                busca=busca.filter(User.status==status_)
            if(habilidade_!=None):
                busca=busca.filter(User.habilidades.contains(habilidade_))
            return self.loop_busca(busca.all(),mais_votado_)
     
    def buscar(self,ator_=None,personagem_=None):
        if(len(str(ator_).split())<=3):
            #verifica se tem 
            print("ola")
            return 
        with Session(engine) as session:

            if(ator_!=None and ator_!="" ):  
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.ator.ilike(f"{ator_}%")).first()
                    
                if(dados!= None):
                        return {"nome":dados[0],"ator":dados[1],"status":dados[2],"habilidade":dados[3],"upvote":dados[4]}
                else:
                    return None
            else:
                dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.nome.ilike(f"{personagem_}%")).first()
                if(dados!=None):
                    return {"nome":dados[0],"ator":dados[1],"status":dados[2],"habilidade":dados[3],"upvote":dados[4]}
                else:
                    return None
    def loop_busca(self,dados_,mais_votado:bool):
        lista=list()

        if(dados_==None):
            return None
        try:
            for c in range(0,len(dados_)):
                            
                lista.append({"nome":dados_[c][0],"ator":dados_[c][1],"status":dados_[c][2],
                    "habilidade":dados_[c][3],"upvote":dados_[c][4]})
            if(mais_votado==True):
                
                maior=0
                personagem=""
                for c in range(0,len(lista)):
                    if(maior<=lista[c]["upvote"]):
                        maior=lista[c]["upvote"]
                        personagem=lista[c]
                    else:
                        continue
                return personagem
            return lista
        except Exception as e:
            print(f"erro em consulta.py {e}")
            return lista
    def atualizar_voto(self,personagem):
        with Session(engine) as session: 
            ##
            #esse User.ator.ilike ele nao faz diferenciaçao entre maiusculo ou minusculo 
            #  se tiver  john como parametro e aparecer jjjjohnnn ele vai pegar como se fosse 
            #john
            #  ##
            try:
                #contagem=session.query(User.upvote).filter(User.nome.ilike(f"{personagem}%"))
                smt=(update(User).filter(User.nome.ilike(f"{personagem}%")).values(upvote=User.upvote+1))
                session.execute(smt)
                session.commit() 
                if(smt==None):
                    return None
            except Exception as e:
                print(f"erro consulta.py {e}")
                return 2
            return 0
   


