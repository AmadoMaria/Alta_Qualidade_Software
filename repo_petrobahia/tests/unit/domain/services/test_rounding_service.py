import pytest
from domain.services.rounding_service import RoundingService
from domain.entities.produto import TipoProduto


class TestRoundingService:

    def setup_method(self):
        self.service = RoundingService()

    def test_round_price_diesel_to_integer(self):
        result = self.service.round_price(1234.56, TipoProduto.DIESEL)
        assert result == 1235.0

    def test_round_price_diesel_rounds_down(self):
        result = self.service.round_price(1234.49, TipoProduto.DIESEL)
        assert result == 1234.0

    def test_round_price_diesel_rounds_up(self):
        result = self.service.round_price(1234.50, TipoProduto.DIESEL)
        assert result == 1235.0

    def test_round_price_diesel_already_integer(self):
        result = self.service.round_price(1234.0, TipoProduto.DIESEL)
        assert result == 1234.0

    def test_round_price_diesel_with_small_decimal(self):
        result = self.service.round_price(1234.01, TipoProduto.DIESEL)
        assert result == 1234.0

    def test_round_price_diesel_with_large_decimal(self):
        result = self.service.round_price(1234.99, TipoProduto.DIESEL)
        assert result == 1235.0

    def test_round_price_gasolina_to_two_decimals(self):
        result = self.service.round_price(1234.567, TipoProduto.GASOLINA)
        assert result == 1234.57

    def test_round_price_gasolina_rounds_down(self):
        result = self.service.round_price(1234.564, TipoProduto.GASOLINA)
        assert result == 1234.56

    def test_round_price_gasolina_rounds_up(self):
        result = self.service.round_price(1234.565, TipoProduto.GASOLINA)
        assert result == 1234.57

    def test_round_price_gasolina_already_two_decimals(self):
        result = self.service.round_price(1234.56, TipoProduto.GASOLINA)
        assert result == 1234.56

    def test_round_price_etanol_to_two_decimals(self):
        result = self.service.round_price(1234.567, TipoProduto.ETANOL)
        assert result == 1234.57

    def test_round_price_etanol_rounds_down(self):
        result = self.service.round_price(1234.564, TipoProduto.ETANOL)
        assert result == 1234.56

    def test_round_price_etanol_rounds_up(self):
        result = self.service.round_price(1234.565, TipoProduto.ETANOL)
        assert result == 1234.57

    def test_round_price_lubrificante_to_two_decimals(self):
        result = self.service.round_price(1234.567, TipoProduto.LUBRIFICANTE)
        assert result == 1234.57

    def test_round_price_lubrificante_rounds_down(self):
        result = self.service.round_price(1234.564, TipoProduto.LUBRIFICANTE)
        assert result == 1234.56

    def test_round_price_lubrificante_rounds_up(self):
        result = self.service.round_price(1234.565, TipoProduto.LUBRIFICANTE)
        assert result == 1234.57

    def test_round_price_diesel_zero(self):
        result = self.service.round_price(0.0, TipoProduto.DIESEL)
        assert result == 0.0

    def test_round_price_gasolina_zero(self):
        result = self.service.round_price(0.0, TipoProduto.GASOLINA)
        assert result == 0.0

    def test_round_price_diesel_small_value(self):
        result = self.service.round_price(0.49, TipoProduto.DIESEL)
        assert result == 0.0

    def test_round_price_diesel_rounds_up_at_half(self):
        result = self.service.round_price(0.50, TipoProduto.DIESEL)
        assert result == 0.0

    def test_round_price_diesel_rounds_up_above_half(self):
        result = self.service.round_price(0.51, TipoProduto.DIESEL)
        assert result == 1.0

    def test_round_price_gasolina_small_value(self):
        result = self.service.round_price(0.004, TipoProduto.GASOLINA)
        assert result == 0.0

    def test_round_price_gasolina_at_rounding_boundary(self):
        result = self.service.round_price(0.005, TipoProduto.GASOLINA)
        assert result == 0.01

    def test_round_price_with_many_decimals(self):
        result = self.service.round_price(1234.56789123456, TipoProduto.GASOLINA)
        assert result == 1234.57

    def test_round_price_diesel_large_value(self):
        result = self.service.round_price(999999.99, TipoProduto.DIESEL)
        assert result == 1000000.0

    def test_round_price_gasolina_large_value(self):
        result = self.service.round_price(999999.999, TipoProduto.GASOLINA)
        assert result == 1000000.0

    @pytest.mark.parametrize("price,expected", [
        (100.0, 100.0),
        (100.4, 100.0),
        (100.5, 100.0),
        (100.6, 101.0),
        (99.5, 100.0),
        (99.4, 99.0),
    ])
    def test_round_price_diesel_various_values(self, price, expected):
        result = self.service.round_price(price, TipoProduto.DIESEL)
        assert result == expected

    @pytest.mark.parametrize("price,expected", [
        (100.001, 100.0),
        (100.004, 100.0),
        (100.005, 100.01),
        (100.006, 100.01),
        (100.554, 100.55),
        (100.555, 100.56),
        (100.556, 100.56),
    ])
    def test_round_price_gasolina_various_values(self, price, expected):
        result = self.service.round_price(price, TipoProduto.GASOLINA)
        assert result == expected

    @pytest.mark.parametrize("tipo_produto", [
        TipoProduto.GASOLINA,
        TipoProduto.ETANOL,
        TipoProduto.LUBRIFICANTE,
    ])
    def test_round_price_non_diesel_products_use_two_decimals(self, tipo_produto):
        result = self.service.round_price(123.456, tipo_produto)
        assert result == 123.46

    def test_round_price_diesel_negative_value(self):
        result = self.service.round_price(-100.6, TipoProduto.DIESEL)
        assert result == -101.0

    def test_round_price_gasolina_negative_value(self):
        result = self.service.round_price(-100.566, TipoProduto.GASOLINA)
        assert result == -100.57
