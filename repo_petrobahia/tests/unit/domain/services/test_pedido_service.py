import pytest
from unittest.mock import Mock
from domain.services.pedido_service import PedidoService
from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto
from domain.entities.cliente import Cliente


class TestPedidoService:

    def setup_method(self):
        self.mock_pedido_repository = Mock()
        self.mock_cliente_repository = Mock()
        self.service = PedidoService(
            self.mock_pedido_repository,
            self.mock_cliente_repository
        )

        self.valid_cliente = Cliente(
            id="client-123",
            nome="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

    def test_process_pedido_successful(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-001",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100,
            cupom=None
        )

        assert pedido.id == "pedido-001"
        assert pedido.cliente_id == "client-123"
        assert pedido.tipo_produto == TipoProduto.DIESEL
        assert pedido.quantidade == 100
        assert price == 399.0

    def test_process_pedido_with_coupon(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-002",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100,
            cupom="MEGA10"
        )

        expected_price = 399.0 * 0.9
        assert price == expected_price

    def test_process_pedido_raises_error_if_customer_not_found(self):
        self.mock_cliente_repository.find_by_id.return_value = None

        with pytest.raises(ValueError, match="Customer not found"):
            self.service.process_pedido(
                id="pedido-003",
                cliente_id="nonexistent",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=100
            )

    def test_process_pedido_raises_error_on_zero_quantity(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente

        with pytest.raises(ValueError, match="Quantity must be positive"):
            self.service.process_pedido(
                id="pedido-004",
                cliente_id="client-123",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=0
            )

    def test_process_pedido_raises_error_on_negative_quantity(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente

        with pytest.raises(ValueError, match="Quantity must be positive"):
            self.service.process_pedido(
                id="pedido-005",
                cliente_id="client-123",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=-10
            )

    def test_process_pedido_raises_error_on_save_failure(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = False

        with pytest.raises(Exception, match="Failed to save order"):
            self.service.process_pedido(
                id="pedido-006",
                cliente_id="client-123",
                tipo_produto=TipoProduto.DIESEL,
                quantidade=100
            )

    def test_process_pedido_applies_diesel_volume_discount(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-007",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=600
        )

        expected_price = (3.99 * 600) * 0.95
        assert price == expected_price

    def test_process_pedido_applies_gasolina_volume_discount(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-008",
            cliente_id="client-123",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=250
        )

        expected_price = round((5.19 * 250) - 100.00, 2)
        assert price == expected_price

    def test_process_pedido_rounds_diesel_to_integer(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-009",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        assert price == 399.0
        assert price == int(price)

    def test_process_pedido_rounds_gasolina_to_two_decimals(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-010",
            cliente_id="client-123",
            tipo_produto=TipoProduto.GASOLINA,
            quantidade=10
        )

        assert price == 51.90
        assert len(str(price).split('.')[-1]) <= 2

    def test_process_pedido_combines_volume_and_coupon_discounts(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-011",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=600,
            cupom="MEGA10"
        )

        base_with_volume = (3.99 * 600) * 0.95
        with_coupon = base_with_volume * 0.9
        expected_price = round(with_coupon, 0)
        assert price == expected_price

    def test_process_pedido_saves_pedido_to_repository(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        self.service.process_pedido(
            id="pedido-012",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        self.mock_pedido_repository.save.assert_called_once()
        saved_pedido = self.mock_pedido_repository.save.call_args[0][0]
        assert isinstance(saved_pedido, Pedido)

    def test_process_pedido_verifies_customer_exists(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        self.service.process_pedido(
            id="pedido-013",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        self.mock_cliente_repository.find_by_id.assert_called_once_with("client-123")

    @pytest.mark.parametrize("tipo_produto,quantidade,expected_base", [
        (TipoProduto.DIESEL, 100, 3.99 * 100),
        (TipoProduto.GASOLINA, 100, 5.19 * 100),
        (TipoProduto.ETANOL, 50, 3.59 * 50),
        (TipoProduto.LUBRIFICANTE, 10, 25.00 * 10),
    ])
    def test_process_pedido_calculates_correct_prices(self, tipo_produto, quantidade, expected_base):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-test",
            cliente_id="client-123",
            tipo_produto=tipo_produto,
            quantidade=quantidade
        )

        if tipo_produto == TipoProduto.DIESEL:
            assert price == round(expected_base, 0)
        else:
            assert price == round(expected_base, 2)

    def test_process_pedido_returns_tuple_of_pedido_and_price(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        result = self.service.process_pedido(
            id="pedido-014",
            cliente_id="client-123",
            tipo_produto=TipoProduto.DIESEL,
            quantidade=100
        )

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], Pedido)
        assert isinstance(result[1], (int, float))

    def test_process_pedido_with_lubrificante_and_lub2_coupon(self):
        self.mock_cliente_repository.find_by_id.return_value = self.valid_cliente
        self.mock_pedido_repository.save.return_value = True

        pedido, price = self.service.process_pedido(
            id="pedido-015",
            cliente_id="client-123",
            tipo_produto=TipoProduto.LUBRIFICANTE,
            quantidade=10,
            cupom="LUB2"
        )

        expected_price = round((25.00 * 10) - 2.00, 2)
        assert price == expected_price
