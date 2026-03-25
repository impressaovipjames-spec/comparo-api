from pydantic import BaseModel
from typing import Optional

class Oferta(BaseModel):
    titulo: str
    preco_produto: float
    frete: Optional[float] = 0.0
    total_real: Optional[float] = 0.0
    prazo_dias: Optional[int] = 0
    reputacao: Optional[float] = 0.0
    loja: str
    score_final: Optional[float] = 0.0
    analise_preco: Optional[dict] = None
    link_compra: Optional[str] = None
    link_original: Optional[str] = None
    link_afiliado: Optional[str] = None
    fonte_loja: Optional[str] = None
