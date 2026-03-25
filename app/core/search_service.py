import json
import asyncio
from typing import List
from .adapters.mercadolivre_adapter import MercadoLivreAdapter
from .adapters.amazon_adapter import AmazonAdapter
from .adapters.magalu_adapter import MagaluAdapter
from .adapters.shopee_adapter import ShopeeAdapter
from .models.oferta import Oferta
from .cache import get, setex
from .score import CalculadoraScore
from .detector_preco import DetectorPreco
from .affiliate_service import AffiliateService

async def buscar_produto(query: str, cep: str) -> List[Oferta]:
    cache_key = f"busca:{query}:{cep}"
    
    # 1. Verificar Cache
    cached_data = get(cache_key)
    if cached_data:
        print(f"DEBUG: Retornando resultados do cache para {cache_key}")
        data = json.loads(cached_data)
        return [Oferta(**item) for item in data]
    
    # 2. Consultar Adapters Reais em Paralelo
    adapters = [
        MercadoLivreAdapter(),
        AmazonAdapter(),
        MagaluAdapter(),
        ShopeeAdapter()
    ]
    
    # Dispara todas as buscas simultaneamente
    tasks = [adapter.buscar(query, cep) for adapter in adapters]
    repositorios_resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    results = []
    for r in repositorios_resultados:
        if isinstance(r, list):
            results.extend(r)
        else:
            print(f"Erro em um dos adapters: {r}")
    
    # 3. Aplicar Score, Análise de Preço e Tracking de Afiliados
    if results:
        for r in results:
            # Score inteligente
            CalculadoraScore.calcular(r)
            # Detector de manipulação
            r.analise_preco = DetectorPreco.analisar(query, r.loja, r.total_real)
            
            # Gerar Tracking e Afiliado (Sprint 14)
            r.link_original = r.link_compra
            r.link_afiliado = AffiliateService.gerar_link_afiliado(r.link_compra, r.loja)
            r.link_compra = r.link_afiliado # App usa este para o botão
        
        # Ordenar por score (maior score_final é melhor)
        results.sort(key=lambda x: x.score_final, reverse=True)
        
        # Selecionar Top 3
        results = results[:3]
        
        # 4. Salvar no Cache
        json_results = json.dumps([r.model_dump() for r in results])
        setex(cache_key, json_results, ttl=600)
    
    return results
