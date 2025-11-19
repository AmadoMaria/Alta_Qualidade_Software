from adapters.notifications.console_notification import ConsoleNotification
from adapters.repositories.json_cliente_repository import (
    JsonClienteRepository,
)
from adapters.repositories.json_pedido_repository import JsonPedidoRepository
from adapters.use_cases import (
    ProcessPedidoRequest,
    ProcessPedidoUseCase,
    RegisterClienteRequest,
    RegisterClienteUseCase,
)
from domain.entities.cupom import Cupom


class PetroBahiaCLI:
    def __init__(self) -> None:
        self._cliente_repository = JsonClienteRepository()
        self._pedido_repository = JsonPedidoRepository()
        self._notification_service = ConsoleNotification()

        self._register_cliente_use_case = RegisterClienteUseCase(
            self._cliente_repository, self._notification_service
        )
        self._process_pedido_use_case = ProcessPedidoUseCase(
            self._pedido_repository, self._cliente_repository
        )

    def run_sample_data(self) -> None:
        print("=" * 60)
        print("PetroBahia S.A. - Order Processing System")
        print("=" * 60)
        print()

        clientes_data = [
            {
                "nome": "TransLog",
                "email": "contato@translog.com.br",
                "cnpj": "12345678000190",
            },
            {
                "nome": "MoveMais",
                "email": "vendas@movemais.com",
                "cnpj": "98765432000111",
            },
            {
                "nome": "EcoFrota",
                "email": "suporte@ecofrota.com.br",
                "cnpj": "11223344000155",
            },
            {
                "nome": "PetroPark",
                "email": "comercial@petropark.com",
                "cnpj": "55667788000199",
            },
        ]

        print("Registering customers...")
        print("-" * 60)
        registered_clientes = []
        for cliente_data in clientes_data:
            request = RegisterClienteRequest(
                nome=cliente_data["nome"],
                email=cliente_data["email"],
                cnpj=cliente_data["cnpj"],
            )
            response = self._register_cliente_use_case.execute(request)
            if response.success:
                registered_clientes.append(response.cliente)
                print(f"✓ {response.cliente.nome} registered successfully")
            else:
                print(f"✗ Failed: {response.message}")

        print()
        print("Processing orders...")
        print("-" * 60)

        pedidos_data = [
            {
                "id": "ORD001",
                "cliente_id": registered_clientes[0].id,
                "tipo_produto": "diesel",
                "quantidade": 1200,
                "cupom": Cupom.MEGA10.value.codigo,
            },
            {
                "id": "ORD002",
                "cliente_id": registered_clientes[1].id,
                "tipo_produto": "gasolina",
                "quantidade": 300,
                "cupom": None,
            },
            {
                "id": "ORD003",
                "cliente_id": registered_clientes[2].id,
                "tipo_produto": "etanol",
                "quantidade": 50,
                "cupom": Cupom.NOVO5.value.codigo,
            },
            {
                "id": "ORD004",
                "cliente_id": registered_clientes[3].id,
                "tipo_produto": "lubrificante",
                "quantidade": 12,
                "cupom": Cupom.LUB2.value.codigo,
            },
        ]

        totals = []
        for pedido_data in pedidos_data:
            request = ProcessPedidoRequest(
                id=pedido_data["id"],
                cliente_id=pedido_data["cliente_id"],
                tipo_produto=pedido_data["tipo_produto"],
                quantidade=pedido_data["quantidade"],
                cupom=pedido_data["cupom"],
            )
            response = self._process_pedido_use_case.execute(request)

            if response.success:
                totals.append(response.total)
                cupom_text = (
                    f" (Coupon: {pedido_data['cupom']})" if pedido_data["cupom"] else ""
                )
                print(
                    f"✓ Order {pedido_data['id']}: "
                    f"{pedido_data['tipo_produto'].capitalize()} "
                    f"x{pedido_data['quantidade']}{cupom_text} "
                    f"= R$ {response.total}"
                )
            else:
                print(f"✗ Order {pedido_data['id']} failed: {response.message}")

        print()
        print("-" * 60)
        print(f"TOTAL: R$ {sum(totals)}")
        print("=" * 60)


def main() -> None:
    cli = PetroBahiaCLI()
    cli.run_sample_data()


if __name__ == "__main__":
    main()
