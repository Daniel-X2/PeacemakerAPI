from pydantic import BaseModel, Field

class ElencoDto(BaseModel):
    """
    Data Transfer Object para representar um personagem/ator do elenco.
    
    Attributes:
        nome (str): Nome do personagem (mínimo 3 caracteres).
        ator (str): Nome do ator (mínimo 3 caracteres).
        vivo (bool): Status de vida do personagem.
        habilidades (list): Lista de habilidades do personagem.
        upvote (int): Quantidade de votos recebidos.
    """
    nome: str = Field(min_length=3)
    ator: str = Field(min_length=3)
    vivo: bool
    habilidades: list
    upvote: int

def serializar_lista(dados: list) -> list:
    """
    Converte uma lista de objetos Elenco em uma lista de dicionários.
    
    Args:
        dados (list): Lista de objetos Elenco do banco de dados.
        
    Returns:
        list: Lista de dicionários contendo os dados serializados.
    """
    lista = list()
    for c in dados:
        lista.append(
            ElencoDto(
                nome=c.nome,
                ator=c.ator,
                vivo=c.vivo,
                habilidades=c.habilidades,
                upvote=c.upvote
            ).model_dump()
        )
    return lista

def serializar_dict(dados: list) -> dict:
    """
    Converte uma lista de objetos Elenco em um dicionário ordenado com posições.
    
    Útil para gerar rankings onde a chave é a posição (1° lugar, 2° lugar, etc).
    
    Args:
        dados (list): Lista de objetos Elenco do banco de dados (já ordenados).
        
    Returns:
        dict: Dicionário com as posições como chaves e dados como valores.
    """
    dici = dict()
    for n, c in enumerate(dados):
        dici[f"{n+1}° lugar"] = (
            ElencoDto(
                nome=c.nome,
                ator=c.ator,
                vivo=c.vivo,
                habilidades=c.habilidades,
                upvote=c.upvote
            ).model_dump()
        )
    return dici