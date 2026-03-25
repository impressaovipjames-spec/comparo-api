import httpx
from typing import List
from .base_adapter import BaseAdapter
from ..models.oferta import Oferta

class ShopeeAdapter(BaseAdapter):
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        # Shopee conector simulado com links reais de busca
        return [
            Oferta(
                titulo=f"{query} na Shopee",
                preco_produto=1850.0,
                frete=25.0,
                total_real=1875.0,
                prazo_dias=10,
                reputacao=4.2,
                loja="Shopee",
                link_compra=f"https://shopee.com.br/search?keyword={query.replace(' ', '+')}"
            )
        ]

    async def buscar_preco_apenas(self, query: str) -> float:
        return 1875.0
