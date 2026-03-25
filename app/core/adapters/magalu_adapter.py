import httpx
from typing import List
from .base_adapter import BaseAdapter
from ..models.oferta import Oferta

class MagaluAdapter(BaseAdapter):
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        # Magalu conector simulado com links reais de busca
        return [
            Oferta(
                titulo=f"{query} no Magalu",
                preco_produto=2100.0,
                frete=12.90,
                total_real=2112.90,
                prazo_dias=4,
                reputacao=4.7,
                loja="Magalu",
                link_compra=f"https://www.magazineluiza.com.br/busca/{query.replace(' ', '+')}"
            )
        ]

    async def buscar_preco_apenas(self, query: str) -> float:
        return 2112.90
