from sqlalchemy import update
from sqlalchemy.orm import Session
from banco import engine
from models import User

class consulta():
    def __init__(self):
        pass
    
    def buscar_no_elenco(self,habilidade:str=None,ator:str=None,personagem:str=None,status=None,mais_votado=False):
        with Session(engine) as session:
            if(ator==None and personagem ==None):
            # #
            # aqui faz a filtragem da pesquisa
            # #
                try:

                    busca=session.query(User.nome,User.ator,User.status,
                    User.habilidades,User.upvote)
                except Exception as e:
                    print(f"erro consulta.py {e}")
                    return None
                if(status==None and habilidade==None and mais_votado==False):
                        #aqui serve principalmente pra listar todos no elenco
                    return busca.all()
                if(status!=None):
                    busca=busca.filter(User.status==status)
                if(habilidade!=None):
                    busca=busca.filter(User.habilidades.contains(habilidade))
                if(mais_votado==True):
                        #ainda vou implementar calma manito
                    print
                lista=list()
                
                busca=busca.all()
                if(busca==None):
                    return None
                try:
                    for c in range(0,len(busca)):
                            
                        lista.append({"nome":busca[c][0],"ator":busca[c][1],"status":busca[c][2],
                        "habilidade":busca[c][3],"upvote":busca[c][4]})
                    return lista
                except IndexError:
                    for c in range(0,busca.count()):
                        lista.append({"nome":busca[c][0],"ator":busca[c][1],"status":busca[c][2],
                        "habilidade":busca[c][3],"upvote":busca[c][4]})
                    return lista
            else:
                if(ator!=None):
                
                    dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.ator.ilike(f"{ator}%")).first()
                    
                    if(dados!= None):
                        return {"nome":dados[0],"ator":dados[1],"status":dados[2],"habilidade":dados[3],"upvote":dados[4]}
                    else:
                        return None
                else:
                    dados=session.query(User.nome,User.ator,User.status,User.habilidades,User.upvote).filter(User.nome.ilike(f"{personagem}%")).first()
                    if(dados!=None):
                        return {"nome":dados[0][0],"ator":dados[0][1],"status":dados[0][2],"habilidade":dados[0][3],"upvote":dados[0][4]}
                    else:
                        return None            
    def atualizar_voto(self,personagem):
         with Session(engine) as session:
            ##
            #esse User.ator.ilike ele nao faz diferenciaçao entre maiusculo ou minusculo 
            #  se tiver  john como parametro e aparecer jjjjohnnn ele vai pegar como se fosse 
            #john
            #  ##
            try:
                contagem=session.query(User.upvote).filter(User.nome.ilike(f"{personagem}%"))
                atualizacao=update(User).filter(User.nome.ilike(f"{personagem}%")).values(upvote=contagem[0][0]+1)   
                session.execute(atualizacao)
                session.commit() 
                if(contagem==None):
                    return None
            except Exception as e:
                print(f"erro consulta.py {e}")
                return 2
            return 0
    
      
            
#n1=consulta()
#n1.buscar_no_elenco(ator="iudaniel")
