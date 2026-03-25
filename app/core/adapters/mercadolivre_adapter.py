import httpx
from typing import List
from .base_adapter import BaseAdapter
from ..models.oferta import Oferta

class MercadoLivreAdapter(BaseAdapter):
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                return []
            
            data = response.json()
            items = data.get("results", [])[:5]  # Pega as primeiras 5
            
            ofertas = []
            for item in items:
                preco = float(item.get("price", 0))
                # Mercado Livre API não dá frete exato sem token/user, então estimamos ou usamos flag
                frete = 0.0 if item.get("shipping", {}).get("free_shipping") else 15.0
                
                ofertas.append(Oferta(
                    titulo=item.get("title"),
                    preco_produto=preco,
                    frete=frete,
                    total_real=preco + frete,
                    prazo_dias=3,  # Estimativa padrão ML
                    reputacao=4.5, # Placeholder (precisaria de outra chamada p/ seller)
                    loja="Mercado Livre",
                    link_compra=item.get("permalink")
                ))
            return ofertas

    async def buscar_preco_apenas(self, query: str) -> float:
        ofertas = await self.buscar(query, "")
        if ofertas:
            return ofertas[0].total_real
        return 0.0
