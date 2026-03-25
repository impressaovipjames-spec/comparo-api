import httpx
from typing import List
from .base_adapter import BaseAdapter
from ..models.oferta import Oferta

class AmazonAdapter(BaseAdapter):
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        # Amazon requer scraping mais complexo ou API. 
        # Para o MVP, faremos um mock de dados reais simulando a estrutura que viria do scraping.
        # Em produção, usaríamos algo como Selenium ou um serviço de Proxy/Scraper.
        
        # Simulação de dados reais da Amazon para a query
        return [
            Oferta(
                titulo=f"{query} na Amazon",
                preco_produto=1999.0,
                frete=0.0,
                total_real=1999.0,
                prazo_dias=2,
                reputacao=4.8,
                loja="Amazon",
                link_compra=f"https://www.amazon.com.br/s?k={query.replace(' ', '+')}"
            )
        ]

    async def buscar_preco_apenas(self, query: str) -> float:
        return 1999.0
