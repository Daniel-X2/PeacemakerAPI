
from sqlalchemy import String
from sqlalchemy import INTEGER
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column



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
    