from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import uuid

class AlertaBase(BaseModel):
    device_id: str
    fcm_token: str
    produto_query: str
    lojas_monitorar: List[str]
    preco_alvo: Optional[float] = None
    queda_percentual: Optional[float] = None
    preco_referencia: float
    status: str = "ativo"

    @field_validator('preco_alvo', 'queda_percentual')
    @classmethod
    def check_alert_criteria(cls, v, info):
        # Esta validação será reforçada no nível de criação (CreateRequest)
        return v

class AlertaCreate(AlertaBase):
    @field_validator('preco_alvo')
    @classmethod
    def validate_criteria(cls, v, info):
        # Acesso via info.data para Pydantic v2
        data = info.data
        if v is None and data.get('queda_percentual') is None:
            raise ValueError('O alerta deve ter preco_alvo OU queda_percentual')
        return v

class AlertaRead(AlertaBase):
    id: uuid.UUID
    criado_em: datetime
