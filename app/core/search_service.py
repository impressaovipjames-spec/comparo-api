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
from .relevancia import validar_relevancia
from .affiliate_service import AffiliateService

async def buscar_produto(query: str, cep: str) -> List[Oferta]:
    cache_key = f"busca:{query}:{cep}"
    
    # 1. Verificar Cache
    cached_data = get(cache_key)
    if cached_data:
        print(f"DEBUG: Retornando resultados do cache para {cache_key}")
        data = json.loads(cached_data)
        return [Oferta(**item) for item in data]
    
    # 2. Consultar Adapters em Paralelo (ML traz 50 resultados agora)
    adapters = [
        MercadoLivreAdapter(),
        AmazonAdapter(),
        MagaluAdapter(),
        ShopeeAdapter()
    ]
    
    tasks = [adapter.buscar(query, cep) for adapter in adapters]
    repositorios_resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_results = []
    for r in repositorios_resultados:
        if isinstance(r, list):
            all_results.extend(r)
    
    if not all_results:
        return []

    # 3. FILTRAR RELEVÂNCIA (Garantir o produto exato)
    relevantes = [
        o for o in all_results 
        if validar_relevancia(o.titulo, query)
    ]
    
    if not relevantes:
        # Se nada for 100% relevante com tokens críticos, voltamos ao original para não dar tela vazia, 
        # mas marcamos como menos confiáveis ou apenas retornamos vazio se a regra for rígida.
        # Seguindo a regra máxima: TOP 3 deve ser o produto EXATO.
        return []

    # 4. FILTRAR SUSPEITOS (Anti-Golpe: < 40% da média dos relevantes)
    media_preco = sum(o.preco_produto for o in relevantes) / len(relevantes)
    confiaveis = [
        o for o in relevantes 
        if o.preco_produto >= (media_preco * 0.4)
    ]

    # 5. Aplicar Score e Serviços Adicionais
    for r in confiaveis:
        # Score inteligente (Preço domina, bônus max 8%)
        CalculadoraScore.calcular(r)
        
        # Detector de manipulação (Comparação histórica)
        r.analise_preco = DetectorPreco.analisar(query, r.loja, r.total_real)
        
        # Links de Afiliado
        r.link_original = r.link_compra
        r.link_afiliado = AffiliateService.gerar_link_afiliado(r.link_compra, r.loja)
        r.link_compra = r.link_afiliado
    
    # 6. ORDENAR PELO SCORE (Quanto menor o score_final, melhor a oferta)
    confiaveis.sort(key=lambda x: x.score_final)
    
    # 7. Regra Final: Garantir que o menor preço absoluto não seja ignorado
    # Se a oferta no Top 1 for > 15% mais cara que o menor preço absoluto da lista, 
    # forçamos o menor preço de volta ao topo.
    menor_preco_absoluto = min(confiaveis, key=lambda x: x.total_real)
    if confiaveis[0].total_real > (menor_preco_absoluto.total_real * 1.15):
        # Move o menor preço para o topo se ele foi "vencido" injustamente por bônus
        confiaveis.remove(menor_preco_absoluto)
        confiaveis.insert(0, menor_preco_absoluto)

    # Selecionar Top 3
    final_top_3 = confiaveis[:3]
    
    # 8. Salvar no Cache
    json_results = json.dumps([r.model_dump() for r in final_top_3])
    setex(cache_key, json_results, ttl=600)
    
    return final_top_3
