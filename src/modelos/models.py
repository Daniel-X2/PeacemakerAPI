from sqlalchemy import String, Boolean
from sqlalchemy import INTEGER
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    """
    Classe base para todos os modelos SQLAlchemy.
    
    Serve como declarative base para a definição de tabelas
    e relacionamentos no banco de dados.
    """
    pass

class Elenco(Base):
    """
    Modelo de banco de dados para representar um personagem do elenco.
    
    Attributes:
        id (int): Identificador único do personagem (chave primária).
        nome (str): Nome do personagem (máximo 30 caracteres).
        ator (str): Nome do ator que interpreta o personagem (máximo 30 caracteres).
        vivo (bool): Status de vida do personagem (True = vivo, False = morto).
        habilidades (list): Lista em formato JSON com as habilidades do personagem.
        upvote (int): Contador de votos recebidos pelo personagem.
    """
    __tablename__ = "elenco"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30))
    ator: Mapped[str] = mapped_column(String(30))
    vivo: Mapped[bool] = mapped_column(Boolean)
    habilidades: Mapped[list] = mapped_column(JSON)
    upvote: Mapped[int] = mapped_column(INTEGER)


