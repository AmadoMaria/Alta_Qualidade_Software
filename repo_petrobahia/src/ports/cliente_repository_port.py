from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.cliente import Cliente


class ClienteRepositoryPort(ABC):
    @abstractmethod
    def save(self, cliente: Cliente) -> bool:
        pass

    @abstractmethod
    def find_by_id(self, cliente_id: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
