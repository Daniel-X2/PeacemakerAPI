from sqlalchemy import update, select
from sqlalchemy.orm import Session
from banco import engine
from models import Elenco,campos
from erros import *
from pydantic_core import _pydantic_core


# ============================
# REPOSITORY
# ============================
class ElencoRepository:
    def get_all(self):
        with Session(engine) as session:
            smt = select(Elenco)
            resultado = session.scalars(smt).all()
            return resultado

    def get_by_query(self, query):
        with Session(engine) as session:
            return session.scalars(query)

    def get_by_name(self, modo: str, nomee: str):
        validar = len(nomee.strip())
        if validar <= 3:
            raise ErroValorMinimo("nome", 3, 4)

        with Session(engine) as session:
            smt = select(Elenco)

            if modo == "ator":
                smt = smt.filter(Elenco.ator.ilike(f"{nomee}%"))
            else:
                smt = smt.filter(Elenco.nome.ilike(f"{nomee}%"))

            return session.scalars(smt).first()

    def atualizar_voto(self, personagem):
        with Session(engine) as session:
            try:
                smt = (
                    update(Elenco)
                    .filter(Elenco.nome.ilike(f"{personagem}%"))
                    .values(upvote=Elenco.upvote + 1)
                )

                result = session.execute(smt)

                if result.rowcount == 0:
                    raise ErroNenhumResultado("Personagem")

                session.commit()

            except Exception as e:
                raise ErroNoBancoSql(e)


repo = ElencoRepository()


# ============================
# SERVICE
# ============================
class ElencoService:
    def monta_query(self, habilidade=None, status=None, mais_votado=False):
        smt = select(Elenco)

        if status is not None:
            smt = smt.filter(Elenco.status == status)

        if habilidade is not None:
            smt = smt.filter(Elenco.habilidades.contains(habilidade))

        if mais_votado:
            smt = smt.order_by(Elenco.upvote.desc())

        return smt

    def busca_com_filtro(self, habilidade=None, status=None, mais_votado=False):
        query = self.monta_query(habilidade, status, mais_votado)

        resultados = repo.get_by_query(query)

        if mais_votado:
            dado = resultados.first()
            if dado is None:
                raise ErroNenhumResultado("Filtro")
            return self.dto(dado)

        dados = resultados.all()
        return self.loop_busca(dados)

    def loop_busca(self, dados):
        lista = []
        if not dados:
            raise ValorVazio

        for dado in dados:
            try:
                lista.append(self.dto(dado))
            except _pydantic_core.ValidationError:
                raise ValorVazio

        return lista

    def dto(self, dado):
        return campos(
            Nome=dado.nome,
            ator=dado.ator,
            status=dado.status,
            habilidades=dado.habilidades,
            upvote=dado.upvote,
        ).model_dump()

    def buscar_por_nome(self, modo, nome):
        dado = repo.get_by_name(modo, nome)
        if dado is None:
            raise ErroNenhumResultado("Nome")
        return self.dto(dado)

    def atualizar_voto(self, personagem):
        repo.atualizar_voto(personagem)


