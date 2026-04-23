from pydantic_core import _pydantic_core
from src.Repository.Repository import ElencoRepository
from src.dto.dto import ElencoDto, serializar_lista, serializar_dict
from src.Erros_personalizado.erros import *
from src.logger_config import setup_logger

logger = setup_logger("Service")
repository = ElencoRepository()


class ElencoService():
    """
    Serviço responsável pela lógica de negócio relacionada ao elenco.

    Realiza operações como busca, votação, rankings e estatísticas
    dos personagens e atores.
    """

    def __init__(self):
        """Inicializa o serviço de elenco."""
        pass

    def buscar_com_filtro(self, vivo: bool = True, habilidade: str = None, mais_votado: bool = False, page: int = 1, limit: int = 10) :
        """
        Busca personagens aplicando filtros personalizados com suporte a paginação.

        Args:
            vivo (bool): Filtrar por status de vida. Padrão: True.
            habilidade (str): Filtrar por habilidade específica. Padrão: None.
            mais_votado (bool): Retornar apenas o mais votado. Padrão: False.
            page (int): Número da página. Padrão: 1.
            limit (int): Registros por página. Padrão: 10.

        Returns:
            dict: Personagem ou lista de personagens que correspondem aos filtros.

        Raises:
            ErroValorMinimo: Se a habilidade tem menos de 3 caracteres.
            ErroValidacao: Se houver erro na validação dos dados.
            ErroNenhumResultado: Se nenhum personagem atender aos critérios.
        """
        offset = (page - 1) * limit
        smt = repository.get_select()
        smt = repository.filtro_status(status=vivo, smt=smt)
        if (habilidade != None and habilidade != ""):
            if (len(habilidade.strip()) >= 3):
                smt = repository.filtro_habilidades(habilidade=habilidade, smt=smt)
            else:
                raise ErroValorMinimo
        if (mais_votado == True):
            logger.info("Buscando o personagem mais votado.")
            smt = repository.mais_votado(smt=smt)  # depois preciso sicronizar com os outros filtros
            dados = repository.executar_first(smt)
            try:
                return ElencoDto(nome=dados.nome,
                                 ator=dados.ator,
                                 vivo=dados.vivo,
                                 habilidades=dados.habilidades,
                                 upvote=dados.upvote).model_dump()
            except _pydantic_core.ValidationError:
                logger.error("Erro de validação ao processar personagem mais votado.")
                raise ErroValidacao
            except AttributeError:
                logger.warning("Nenhum personagem encontrado com os filtros aplicados.")
                raise ErroNenhumResultado("filtros")
        
        logger.info(f"Buscando elenco com filtros (página {page}, limite {limit}).")
        smt = repository.paginar(smt, limit, offset)
        dados = repository.executar_all(smt)

        if (len(dados) == 0):
            raise ErroNenhumResultado("lista vazia")
        dados = serializar_lista(dados=dados)
        return dados

    def buscar_no_elenco(self, nome: str, modo: str = "ator") -> dict:
        """
        Busca um personagem ou ator específico no elenco.

        Args:
            nome (str): Nome do ator ou personagem a buscar.
            modo (str): Tipo de busca - "ator" ou "personagem". Padrão: "ator".

        Returns:
            dict: Informações do ator ou personagem encontrado.

        Raises:
            ErroValorMinimo: Se o nome tem menos de 3 caracteres.
            ErroNenhumResultado: Se nenhum resultado for encontrado.
            ErroValidacao: Se houver erro na validação dos dados.
        """
        if (len(nome) < 3):
            raise ErroValorMinimo
        smt = repository.get_select()

        if (modo == "ator"):
            smt = repository.buscar_ator(nome, smt)
        else:
            smt = repository.buscar_personagem(nome, smt)
        dados = repository.executar_first(smt)
        try:
            return ElencoDto(nome=dados.nome,
                             ator=dados.ator,
                             vivo=dados.vivo,
                             habilidades=dados.habilidades,
                             upvote=dados.upvote).model_dump()
        except AttributeError:
            raise ErroNenhumResultado("nome")
        except _pydantic_core.ValidationError:
            raise ErroValidacao

    def retornar_elenco(self, page: int = 1, limit: int = 10) -> list:
        """
        Retorna todo o elenco cadastrado no banco de dados com suporte a paginação.

        Args:
            page (int): Número da página. Padrão: 1.
            limit (int): Registros por página. Padrão: 10.

        Returns:
            list: Lista com todos os atores e personagens.

        Raises:
            ValorVazio: Se o elenco estiver vazio.
        """
        offset = (page - 1) * limit
        smt = repository.get_select()
        smt = repository.paginar(smt, limit, offset)
        dados = repository.executar_all(smt)
        if (dados == None or len(dados) == 0):
            raise ValorVazio
        dados = serializar_lista(dados)
        return dados

    def votar(self, nome: str) -> None:
        """
        Registra um voto para um personagem específico.

        Args:
            nome (str): Nome do personagem a votar.

        Raises:
            ErroValorMinimo: Se o nome tem menos de 3 caracteres.
        """
        if (len(nome) < 3):
            raise ErroValorMinimo
        logger.info(f"Registrando voto para o personagem: {nome}")
        return repository.update_voto(nome)
        
    def stats(self) -> dict:
        """
        Retorna estatísticas gerais do elenco e personagens.

        Returns:
            dict: Dicionário contendo:
                - total de personagens
                - total de personagens vivos
                - total de personagens mortos
                - personagem com maior quantidade de votos
        """
        total_vivos = repository.total_vivos_mortos(vivo=True)
        total_mortos = repository.total_vivos_mortos(vivo=False)

        smt = repository.mais_votado(smt=repository.get_select())
        dados = repository.executar_first(smt)
        total_personagem = repository.total_personagem()

        return {"total de personagens": total_personagem,
                "total de personagens vivos": total_vivos,
                "total de personagens mortos": total_mortos,
                "personagem com maior quantidade de votos": f"{dados.nome} {dados.upvote} votos",
                }

    def ranking(self, top: int) -> dict:
        """
        Retorna o ranking dos personagens mais votados.

        Args:
            top (int): Quantidade de posições no ranking a retornar.

        Returns:
            dict: Dicionário com o ranking ordenado por votos.

        Raises:
            ValorVazio: Se o ranking estiver vazio.
        """
        smt = repository.mais_votado(smt=repository.get_select()).limit(limit=top)
        dados = repository.executar_all(smt)
        if (dados == None or len(dados) == 0):
            raise ValorVazio
        dados = serializar_dict(dados)

        return dados