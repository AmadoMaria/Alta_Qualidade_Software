from domain.entities.cliente import Cliente
from ports.notification_port import NotificationPort


class ConsoleNotification(NotificationPort):
    def send_welcome_email(self, cliente: Cliente) -> bool:
        print(f"[EMAIL] Welcome message sent to {cliente.email}")
        return True

    def send_order_confirmation(
        self, cliente: Cliente, order_id: str, total: str
    ) -> bool:
        print(
            f"[EMAIL] Order confirmation sent to {cliente.email}: "
            f"Order #{order_id}, Total: {total}"
        )
        return True
