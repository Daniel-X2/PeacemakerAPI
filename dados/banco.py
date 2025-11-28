from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
from src.modelos.models import Elenco, Base

from src.Erros_personalizado.erros import *

engine = create_engine("sqlite:///dados/banco.db")
Base.metadata.create_all(engine)


def adicionar_dados_json() -> None:
    """
    Carrega dados do arquivo JSON e popula o banco de dados na inicialização.

    Se o banco já contiver dados, pula a importação.
    Se estiver vazio, lê o arquivo dados.json e insere todos os registros.

    Raises:
        ErroNoBancoSql: Se houver erro ao carregar ou inserir dados no banco.
    """
    with Session(engine) as session:
        if session.query(Elenco).count() > 0:
            print("banco de dados ok")
        else:
            try:
                with open("dados/dados.json", "r") as arquivo:
                    dados_json = json.load(arquivo)
                    lista_dados = list()
                    for c, n in enumerate(dados_json["elenco"]):    
                        dados = Elenco(
                            nome=n["nome"],
                            ator=n["ator"],
                            vivo=n["vivo"],
                            habilidades=n["habilidade"],
                            upvote=n["upvote"]
                        )
                        lista_dados.append(dados)
                    session.add_all(lista_dados)
                    session.commit()
            except Exception as e:
                raise ErroNoBancoSql(e)


