from .models.oferta import Oferta

class CalculadoraScore:
    BONUS_MAX_PCT = 0.08  # Máximo de 8% de bônus sobre o preço

    @staticmethod
    def calcular(oferta: Oferta) -> Oferta:
        total_real = oferta.preco_produto + oferta.frete
        oferta.total_real = total_real
        
        # O score inicial é o próprio preço. Bônus diminuem o score (quanto menor, melhor).
        score = total_real
        
        # Cálculo de Bônus (Até o limite de 8%)
        total_bonus_pct = 0.0
        
        if oferta.prazo_dias <= 3:
            total_bonus_pct += 0.03  # 3% por agilidade
            
        if oferta.reputacao >= 4.8:
            total_bonus_pct += 0.03  # 3% por confiança
            
        if oferta.frete == 0:
            total_bonus_pct += 0.02  # 2% por frete grátis
            
        # Garantir que não ultrapassa o teto de 8%
        total_bonus_pct = min(total_bonus_pct, CalculadoraScore.BONUS_MAX_PCT)
        
        # Aplicar bônus
        score = score * (1 - total_bonus_pct)
            
        # Penalidades ainda existem para afastar ofertas ruins
        if oferta.prazo_dias > 10:
            score *= 1.15
            
        if oferta.reputacao < 4.0:
            score *= 1.10
            
        oferta.score_final = round(score, 2)
        return oferta
