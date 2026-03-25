import asyncio
import os
from datetime import datetime
from core.supabase_client import get_supabase
from core.search_service import buscar_produto

async def coletar_precos():
    """
    Worker que coleta preços dos produtos mais monitorados/populares e salva no histórico.
    """
    supabase = get_supabase()
    
    print(f"[{datetime.now()}] Iniciando coleta diária de preços...")
    
    try:
        # Pega queries únicas dos alertas ativos para monitorar
        response = supabase.table("alertas").select("produto_query").eq("status", "ativo").execute()
        queries = list(set([r['produto_query'] for r in response.data]))
        
        # Se não houver alertas, monitora alguns termos padrão
        if not queries:
            queries = ["iPhone 15", "PlayStation 5", "Notebook Gamer"]
            
        for query in queries:
            print(f"Coletando para: {query}")
            # Mock de CEP para coleta (São Paulo)
            results = await buscar_produto(query, "01310100")
            
            for oferta in results:
                data_historico = {
                    "produto_query": query,
                    "loja": oferta.loja,
                    "preco": oferta.preco_produto,
                    "frete": oferta.frete,
                    "preco_total": oferta.total_real,
                    "coletado_em": datetime.now().date().isoformat()
                }
                
                # Salvar no price_history
                supabase.table("price_history").insert(data_historico).execute()
                
    except Exception as e:
        print(f"Erro na coleta de preços: {e}")

if __name__ == "__main__":
    asyncio.run(coletar_precos())
