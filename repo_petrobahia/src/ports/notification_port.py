from abc import ABC, abstractmethod

from domain.entities.cliente import Cliente


class NotificationPort(ABC):
    @abstractmethod
    def send_welcome_email(self, cliente: Cliente) -> bool:
        pass

    @abstractmethod
    def send_order_confirmation(
        self, cliente: Cliente, order_id: str, total: str
    ) -> bool:
        pass
