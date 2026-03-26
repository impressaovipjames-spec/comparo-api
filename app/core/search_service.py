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
    from ..config import ENABLE_FAKE_ADAPTERS
    
    adapters = [
        MercadoLivreAdapter()
    ]
    
    if ENABLE_FAKE_ADAPTERS:
        adapters.extend([
            AmazonAdapter(),
            MagaluAdapter(),
            ShopeeAdapter()
        ])
    
    print("ADAPTERS ATIVOS:", [type(a).__name__ for a in adapters])
    
    tasks = [adapter.buscar(query, cep) for adapter in adapters]
    repositorios_resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_results = []
    for r in repositorios_resultados:
        if isinstance(r, Exception):
            print("ERRO ADAPTER NO GATHER:", str(r))
            continue
        if isinstance(r, list):
            all_results.extend(r)
            
    print("\n==== DEBUG BUSCA ====")
    print("QUERY:", query)
    print("CEP:", cep)
    print("ADAPTERS ATIVOS:", [type(a).__name__ for a in adapters])
    print("STATUS DAS TASKS GATHER:", ["OK" if isinstance(r, list) else "FALHA" for r in repositorios_resultados])
    print("TOTAL OFERTAS MISTURADAS:", len(all_results))
    print("=====================\n")
    
    if not all_results:
        print("⚠ Nenhuma oferta real encontrada - retornando vazio com segurança!")
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
    
    # 7. Regra Final: Trava de Margem Competitiva (15%)
    # Se a diferença entre a 1ª e a 2ª oferta for > 15%, o PREÇO ABSOLUTO deve mandar.
    # Se houver uma oferta MUITO mais barata em qualquer lugar da lista, ela SOBE.
    if confiaveis:
        menor_pelo_preco = min(confiaveis, key=lambda x: x.total_real)
        if confiaveis[0].total_real > (menor_pelo_preco.total_real * 1.15):
            # Remove de onde estiver e coloca no topo
            confiaveis.remove(menor_pelo_preco)
            confiaveis.insert(0, menor_pelo_preco)

    # 8. Selecionar Top 3 FINAL (Garantindo que a lista está curta)
    final_top_3 = confiaveis[:3]
    
    # 9. Salvar no Cache
    json_results = json.dumps([r.model_dump() for r in final_top_3])
    setex(cache_key, json_results, ttl=600)
    
    return final_top_3
