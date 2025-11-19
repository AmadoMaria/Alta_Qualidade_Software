from ports.cliente_repository_port import ClienteRepositoryPort
from domain.value_objects import CNPJ, Email
from domain.entities.cliente import Cliente
from ports.notification_port import NotificationPort


class ClientService:
    def __init__(
        self,
        cliente_repository: ClienteRepositoryPort,
        notification_service: NotificationPort,
    ):
        self._cliente_repository = cliente_repository
        self._notification_service = notification_service

    def register_client(self, name: str, email: str, cnpj: str):

        cliente = Cliente(
            nome=name,
            email=email,
            cnpj=cnpj,
        )

        if not self._cliente_repository.save(cliente):
            # TODO: Create custom exception
            raise Exception("Failed to save client")

        self._notification_service.send_welcome_email(cliente)

        return cliente
