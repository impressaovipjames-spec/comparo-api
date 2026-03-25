from typing import List
from .base_adapter import BaseAdapter
from core.models.oferta import Oferta

class MockStoreAdapter(BaseAdapter):
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        # Simula um atraso de rede
        import asyncio
        await asyncio.sleep(0.5)
        
        return [
            Oferta(
                titulo="Fone de Ouvido Bluetooth Premium MK-500",
                preco_produto=1250.00,
                frete=15.00,
                prazo_dias=3,
                reputacao=4.9,
                loja="Loja Virtual Alpha"
            ),
            Oferta(
                titulo="Fone Bluetooth Noise Cancelling MK-500",
                preco_produto=1199.90,
                frete=45.00,
                prazo_dias=7,
                reputacao=4.2,
                loja="Marketplace Beta"
            ),
            Oferta(
                titulo="Combo Fone Premium MK-500 + Case",
                preco_produto=1300.00,
                frete=0.00,
                prazo_dias=1,
                reputacao=5.0,
                loja="Express Gamma"
            )
        ]

    async def buscar_preco_apenas(self, query: str) -> float:
        return 1199.90
