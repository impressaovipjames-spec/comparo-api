import asyncio
import time
from datetime import datetime
from core.supabase_client import get_supabase
from core.search_service import buscar_produto
from core.notification_service import NotificationService

async def verificar_alertas():
    """
    Worker que percorre a tabela de alertas ativos, consulta o preço atual 
    e dispara notificações se as condições forem atingidas.
    """
    supabase = get_supabase()
    
    print(f"[{datetime.now()}] Iniciando ciclo de verificação de alertas...")
    
    # 1. Buscar alertas ativos
    try:
        response = supabase.table("alertas").select("*").eq("status", "ativo").execute()
        alertas = response.data
    except Exception as e:
        print(f"Erro ao buscar alertas: {e}")
        return

    if not alertas:
        print("Nenhum alerta ativo encontrado.")
        return

    for alerta in alertas:
        # 2. Consultar preço atual
        try:
            query = alerta['produto_query']
            # Para o worker, usamos um CEP padrão ou o CEP do alerta se tivéssemos salvo (podemos usar um padrão de SP por enquanto)
            # Como o search_service já lida com mock e busca, pegamos o melhor resultado (Top 1)
            results = await buscar_produto(query, "01310100") 
            
            if not results:
                continue
                
            melhor_oferta = results[0]
            preco_atual = melhor_oferta.preco_produto
            
            # 3. Verificar Condições
            disparar = False
            
            # Condição 1: Preço Alvo
            if alerta.get('preco_alvo') and preco_atual <= alerta['preco_alvo']:
                disparar = True
                
            # Condição 2: Queda Percentual
            elif alerta.get('queda_percentual') and alerta.get('preco_referencia'):
                queda_real = ((alerta['preco_referencia'] - preco_atual) / alerta['preco_referencia']) * 100
                if queda_real >= alerta['queda_percentual']:
                    disparar = True
            
            # 4. Enviar Notificação e Atualizar Status
            if disparar:
                print(f"DISPARO: {query} atingiu o preço R$ {preco_atual}")
                NotificationService.enviar_alerta_preco(
                    alerta['fcm_token'], 
                    melhor_oferta.titulo, 
                    preco_atual
                )
                
                # Atualizar status para disparado no Supabase
                supabase.table("alertas").update({"status": "disparado"}).eq("id", alerta['id']).execute()
                
        except Exception as e:
            print(f"Erro ao processar alerta {alerta['id']}: {e}")

    print(f"[{datetime.now()}] Ciclo de verificação finalizado.")

if __name__ == "__main__":
    # Script para rodar o worker manualmente
    while True:
        asyncio.run(verificar_alertas())
        # Aguarda 5 minutos para a próxima verificação (em prod seria via Cron ou Celery)
        time.sleep(300)
