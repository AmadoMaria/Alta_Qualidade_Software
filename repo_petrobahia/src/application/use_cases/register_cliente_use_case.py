from dataclasses import dataclass
from typing import Optional

from domain.entities.cliente import Cliente
from domain.value_objects import CNPJ, Email
from ports.cliente_repository_port import ClienteRepositoryPort
from ports.notification_port import NotificationPort


@dataclass
class RegisterClienteRequest:
    id: str
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
        self._cliente_repository = cliente_repository
        self._notification_service = notification_service

    def execute(self, request: RegisterClienteRequest) -> RegisterClienteResponse:
        try:
            email = Email(request.email)
        except ValueError as e:
            return RegisterClienteResponse(
                success=False,
                message=f"Invalid email: {str(e)}",
            )

        try:
            cnpj = CNPJ(request.cnpj)
        except ValueError as e:
            return RegisterClienteResponse(
                success=False,
                message=f"Invalid CNPJ: {str(e)}",
            )

        if self._cliente_repository.exists_by_email(email.value):
            return RegisterClienteResponse(
                success=False,
                message=f"Email already registered: {email.value}",
            )

        cliente = Cliente(
            id=request.id,
            nome=request.nome,
            email=email.value,
            cnpj=cnpj.value,
        )

        if not self._cliente_repository.save(cliente):
            return RegisterClienteResponse(
                success=False,
                message="Failed to save customer",
            )

        self._notification_service.send_welcome_email(cliente)

        return RegisterClienteResponse(
            success=True,
            message="Customer registered successfully",
            cliente=cliente,
        )
