from ports.cliente_repository_port import ClienteRepositoryPort
from domain.value_objects import CNPJ, Email

class CLientService:
    def __init__(self, cliente_repository: ClienteRepositoryPort):
        self._cliente_repository = cliente_repository

    def register_client(self, name: str, email: str, cnpj: str):
        try:
            email = Email(email)
        except ValueError as e:
            return RegisterClienteResponse(
                success=False,
                message=f"Invalid email: {str(e)}",
            )

        try:
            cnpj = CNPJ(cnpj)
        except ValueError as e:
            return RegisterClienteResponse(
                success=False,
                message=f"Invalid CNPJ: {str(e)}",
            )

        return