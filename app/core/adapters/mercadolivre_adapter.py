import httpx
import os
import certifi
import ssl
from typing import List
from .base_adapter import BaseAdapter
from ..models.oferta import Oferta
from app.core import cache

# Chaves estáticas e iniciais geradas pelo sistema de Auth
ML_APP_ID = "6744427811164510"
ML_SECRET_KEY = "7cqvhfV1gqoISKiwIzyEUDd2vRH6ZSkt"
ML_INITIAL_REFRESH = "TG-69c4754b4c5fab00013d1ae8-40954988"

class MercadoLivreAdapter(BaseAdapter):
    async def _get_access_token(self) -> str:
        # Tenta pegar do cache (dura ~6h)
        token = cache.get("ML_ACCESS_TOKEN")
        if token:
            return token
            
        # Pega o último Refresh Token válido salvo (ou usa o inicial que recebemos)
        refresh_token = cache.get("ML_REFRESH_TOKEN") or ML_INITIAL_REFRESH
        
        # Pede uma nova chave para o Mercado Livre
        url = "https://api.mercadolibre.com/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": ML_APP_ID,
            "client_secret": ML_SECRET_KEY,
            "refresh_token": refresh_token
        }
        
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            async with httpx.AsyncClient(verify=ssl_context) as client:
                resp = await client.post(url, data=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    new_access = data.get("access_token")
                    new_refresh = data.get("refresh_token")
                    
                    # Salva o Access Token por 5h30min (19800 segundos) para evitar que expire na hora da busca
                    cache.setex("ML_ACCESS_TOKEN", new_access, 19800)
                    # Salva o novo Refresh Token permanentemente
                    cache.set_key("ML_REFRESH_TOKEN", new_refresh)
                    
                    return new_access
                else:
                    print("ERRO AO RENOVAR TOKEN DO ML:", resp.text)
                    return ""
        except Exception as e:
            print("EXCEPTION AO RENOVAR TOKEN DO ML:", str(e))
            return ""

    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        token = await self._get_access_token()
        if not token:
            return [] # Falhou feio na autenticação
            
        # Busca usando o Crachá VIP
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&sort=price_asc&limit=50"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            async with httpx.AsyncClient(verify=ssl_context) as client:
                response = await client.get(url, headers=headers)
                if response.status_code == 401:
                    # Token foi revogado antes do cache expirar. Vamos forçar um wipe.
                    cache._redis_client.delete("ML_ACCESS_TOKEN")
                    return []
                    
                if response.status_code != 200:
                    print("ERRO BUSCA ML:", response.text)
                    return []
                
                data = response.json()
                items = data.get("results", [])
                
                ofertas = []
                for item in items:
                    preco = float(item.get("price", 0))
                    frete = 0.0 if item.get("shipping", {}).get("free_shipping") else 15.0
                    
                    ofertas.append(Oferta(
                        titulo=item.get("title"),
                        preco_produto=preco,
                        frete=frete,
                        total_real=preco + frete,
                        prazo_dias=3,
                        reputacao=4.5,
                        loja="Mercado Livre",
                        link_compra=item.get("permalink")
                    ))
                return ofertas
        except Exception as e:
            print("EXCEPTION BUSCA ML:", str(e))
            return []

    async def buscar_preco_apenas(self, query: str) -> float:
        ofertas = await self.buscar(query, "")
        if ofertas:
            return ofertas[0].total_real
        return 0.0
