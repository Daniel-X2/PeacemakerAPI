from src.Service.Service import ElencoService
from dados.banco import adicionar_dados_json
import pytest
adicionar_dados_json()
class Test_service:
    service=ElencoService()
    def test_busca_com_filtro_vivo(self):
        resultado=self.service.buscar_com_filtro(vivo=True)
        assert resultado[0]["vivo"]==True
    def test_busca_com_filtro_habilidade(self):
        resultado=self.service.buscar_com_filtro(habilidade="Matador")
        resultado=str(resultado[0]["habilidades"]).lower()
        assert "matador" in resultado
    def test_busca_com_filtro(self):
        resultado=self.service.buscar_com_filtro(vivo=True,habilidade="Matador",mais_votado=True)
        assert resultado["ator"]=="John Cena"
    def test_busca_no_elenco(self):
        resultado=self.service.buscar_no_elenco("adrian","personagem")
        resultado=str(resultado["nome"]).lower()
        assert "adrian" in resultado 
    def test_retornar_elenco(self):
        resultado=self.service.retornar_elenco()
        assert len(resultado)>0
        assert resultado[0]["ator"]== "John Cena"
    def test_stats(self):
        resultado=self.service.stats()
        assert resultado["total de personagens"]>=5
        assert resultado ["total de personagens vivos"]>=4
    def test_ranking(self):
        resultado=self.service.ranking(3)
        assert len(resultado)==3
        assert resultado["1° lugar"] !=None 
        assert len(resultado["1° lugar"]) >=3
