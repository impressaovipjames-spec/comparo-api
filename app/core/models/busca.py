from pydantic import BaseModel

class BuscaRequest(BaseModel):
    query: str
    cep: str
