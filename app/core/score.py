from .models.oferta import Oferta

class CalculadoraScore:
    @staticmethod
    def calcular(oferta: Oferta) -> Oferta:
        # 1. Custo Direto
        total_real = oferta.preco_produto + oferta.frete
        oferta.total_real = total_real
        
        # Base do score é o total real
        score = total_real
        
        # 2. Ajustes (Bônus diminuem o score, Penalidades aumentam)
        
        # Entrega rápida (<= 3 dias) -> Bônus de 10%
        if oferta.prazo_dias <= 3:
            score *= 0.90
            
        # Reputação Alta (>= 4.8) -> Bônus de 5%
        if oferta.reputacao >= 4.8:
            score *= 0.95
            
        # Frete Grátis -> Bônus de 5%
        if oferta.frete == 0:
            score *= 0.95
            
        # Prazo Longo (> 10 dias) -> Penalidade de 15%
        if oferta.prazo_dias > 10:
            score *= 1.15
            
        # Reputação Baixa (< 4.0) -> Penalidade de 10%
        if oferta.reputacao < 4.0:
            score *= 1.10
            
        oferta.score_final = round(score, 2)
        return oferta
