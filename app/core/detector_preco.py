from datetime import datetime, timedelta
from typing import Dict, List, Optional
from core.supabase_client import get_supabase

class DetectorPreco:
    @staticmethod
    def analisar(produto_query: str, loja: str, preco_atual: float) -> Dict:
        """
        Analisa o preço atual em relação ao histórico dos últimos 30 dias.
        """
        supabase = get_supabase()
        data_limite = (datetime.now() - timedelta(days=30)).date().isoformat()
        
        try:
            # Buscar histórico dos últimos 30 dias
            response = supabase.table("price_history") \
                .select("preco_total") \
                .eq("produto_query", produto_query) \
                .eq("loja", loja) \
                .gte("coletado_em", data_limite) \
                .execute()
            
            historico = [r['preco_total'] for r in response.data]
            
            if len(historico) < 3:
                return {
                    "status": "SEM_HISTORICO",
                    "variacao_percentual": 0,
                    "preco_medio_30d": 0,
                    "preco_minimo_30d": 0,
                    "badge_ui": "Novo por aqui",
                    "badge_cor": "grey"
                }
            
            preco_medio = sum(historico) / len(historico)
            preco_minimo = min(historico)
            variacao = ((preco_atual - preco_medio) / preco_medio) * 100
            
            status = "ESTAVEL"
            badge = "Preço estável"
            cor = "blue"
            
            if preco_atual <= preco_minimo:
                status = "MENOR_HISTORICO"
                badge = "Menor preço em 30 dias!"
                cor = "purple"
            elif variacao <= -10:
                status = "DESCONTO_REAL"
                badge = "Desconto real 🔥"
                cor = "green"
            elif variacao >= 10:
                status = "INFLADO"
                badge = "Preço inflado ⚠️"
                cor = "red"
                
            return {
                "status": status,
                "variacao_percentual": round(variacao, 2),
                "preco_medio_30d": round(preco_medio, 2),
                "preco_minimo_30d": round(preco_minimo, 2),
                "badge_ui": badge,
                "badge_cor": cor
            }
            
        except Exception as e:
            print(f"Erro ao analisar preço: {e}")
            return {"status": "ERRO", "badge_ui": "N/A", "badge_cor": "grey"}
