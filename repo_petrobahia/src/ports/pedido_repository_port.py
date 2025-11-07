from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.pedido import Pedido


class PedidoRepositoryPort(ABC):
    @abstractmethod
    def save(self, pedido: Pedido) -> bool:
        pass

    @abstractmethod
    def find_by_id(self, pedido_id: str) -> Optional[Pedido]:
        pass

    @abstractmethod
    def find_by_cliente_id(self, cliente_id: str) -> List[Pedido]:
        pass
