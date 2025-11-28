from sqlalchemy import update, select, func
from sqlalchemy.orm import Session
from dados.banco import engine, Elenco

class ElencoRepository():
    """
    Repositório responsável pela camada de acesso aos dados do elenco.
    
    Realiza operações de consulta, filtro, atualização e contagem
    de personagens e atores no banco de dados.
    """

    def __init__(self):
        """Inicializa o repositório de elenco."""
        pass
    
    def get_select(self):
        """
        Cria um statement SELECT básico para a tabela Elenco.
        
        Returns:
            Select: Statement SQLAlchemy pronto para ser filtrado e executado.
        """
        smt = select(Elenco)
        return smt

    def mais_votado(self, smt):
        """
        Ordena o statement pelos personagens mais votados em ordem decrescente.
        
        Args:
            smt (Select): Statement SQLAlchemy a ser ordenado.
            
        Returns:
            Select: Statement ordenado por votos (descendente).
        """
        smt = smt.order_by(Elenco.upvote.desc())
        return smt
        
    def filtro_status(self, status, smt):
        """
        Filtra personagens por status de vida (vivo ou morto).
        
        Args:
            status (bool): True para vivos, False para mortos.
            smt (Select): Statement SQLAlchemy a ser filtrado.
            
        Returns:
            Select: Statement com filtro de status aplicado.
        """
        smt = smt.filter(Elenco.vivo == status)
        return smt
        
    def filtro_habilidades(self, habilidade, smt):
        """
        Filtra personagens que possuem uma habilidade específica.
        
        Args:
            habilidade (str): Nome da habilidade a filtrar.
            smt (Select): Statement SQLAlchemy a ser filtrado.
            
        Returns:
            Select: Statement com filtro de habilidade aplicado.
        """
        smt = smt.filter(Elenco.habilidades.contains(habilidade))
        return smt
        
    def executar_all(self, smt):
        """
        Executa um statement e retorna todos os resultados.
        
        Args:
            smt (Select): Statement SQLAlchemy a executar.
            
        Returns:
            list: Lista com todos os resultados encontrados.
        """
        with Session(engine) as session:
            return session.scalars(smt).all()
            
    def executar_first(self, smt):
        """
        Executa um statement e retorna apenas o primeiro resultado.
        
        Args:
            smt (Select): Statement SQLAlchemy a executar.
            
        Returns:
            Elenco: Primeiro resultado encontrado ou None se vazio.
        """
        with Session(engine) as session:
            return session.scalars(smt).first()
            
    def update_voto(self, personagem):
        """
        Incrementa em 1 o contador de votos de um personagem.
        
        Args:
            personagem (str): Nome do personagem a receber o voto.
            
        Returns:
            None
        """
        with Session(engine) as session:
            smt = (update(Elenco).filter(Elenco.nome.ilike(f"{personagem}%")).values(upvote=Elenco.upvote + 1))
            session.execute(smt)
            session.commit()
        
    def buscar_ator(self, nome, smt):
        """
        Filtra personagens pelo nome do ator (busca parcial).
        
        Args:
            nome (str): Nome do ator a buscar.
            smt (Select): Statement SQLAlchemy a ser filtrado.
            
        Returns:
            Select: Statement com filtro de ator aplicado.
        """
        smt = smt.filter(Elenco.ator.ilike(f"{nome}%"))
        return smt
        
    def buscar_personagem(self, nome, smt):
        """
        Filtra personagens pelo nome do personagem (busca parcial).
        
        Args:
            nome (str): Nome do personagem a buscar.
            smt (Select): Statement SQLAlchemy a ser filtrado.
            
        Returns:
            Select: Statement com filtro de personagem aplicado.
        """
        smt = smt.filter(Elenco.nome.ilike(f"{nome}%"))
        return smt
        
    def total_personagem(self):
        """
        Retorna a contagem total de personagens no banco de dados.
        
        Returns:
            int: Total de personagens cadastrados.
        """
        with Session(engine) as session:
            smt = select(func.count(Elenco.id))
            total = session.execute(smt).scalars().first()
            return total
            
    def total_vivos_mortos(self, vivo: bool):
        """
        Conta quantos personagens estão vivos ou mortos.
        
        Args:
            vivo (bool): True para contar vivos, False para contar mortos.
            
        Returns:
            int: Total de personagens vivos ou mortos conforme o filtro.
        """
        with Session(engine) as session:
            smt = select(func.count(Elenco.vivo)).filter(Elenco.vivo == vivo)
            total = session.execute(smt).scalars().first()
            return total



