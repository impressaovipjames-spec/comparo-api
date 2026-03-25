from abc import ABC, abstractmethod
from typing import List
from ..models.oferta import Oferta

class BaseAdapter(ABC):
    @abstractmethod
    async def buscar(self, query: str, cep: str) -> List[Oferta]:
        pass

    @abstractmethod
    async def buscar_preco_apenas(self, query: str) -> float:
        pass
