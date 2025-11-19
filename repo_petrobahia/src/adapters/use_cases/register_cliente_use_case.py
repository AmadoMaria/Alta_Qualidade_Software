from dataclasses import dataclass
from typing import Optional

from domain.entities.cliente import Cliente
from domain.value_objects import CNPJ, Email
from domain.services.client_service import ClientService
from ports.cliente_repository_port import ClienteRepositoryPort
from ports.notification_port import NotificationPort


@dataclass
class RegisterClienteRequest:
    nome: str
    email: str
    cnpj: str


@dataclass
class RegisterClienteResponse:
    success: bool
    message: str
    cliente: Optional[Cliente] = None


class RegisterClienteUseCase:
    def __init__(
        self,
        cliente_repository: ClienteRepositoryPort,
        notification_service: NotificationPort,
    ):
        self._client_service = ClientService(cliente_repository, notification_service)

    def execute(self, request: RegisterClienteRequest) -> RegisterClienteResponse:
        try:
            cliente = self._client_service.register_client(
                request.nome, request.email, request.cnpj
            )
            return RegisterClienteResponse(
                success=True,
                message="Customer registered successfully",
                cliente=cliente,
            )
        except ValueError as e:
            # TODO: Add custom error code to response
            return RegisterClienteResponse(
                success=False,
                message="Failed to register customer",
            )
