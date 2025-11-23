import pytest
from domain.services.pricing_service import PricingService
from domain.entities.produto import TipoProduto


class TestPricingService:

    def setup_method(self):
        self.service = PricingService()

    def test_calculate_price_diesel_no_discount(self):
        result = self.service.calculate_price(TipoProduto.DIESEL, 100)
        expected = 3.99 * 100
        assert result == expected

    def test_calculate_price_diesel_with_5_percent_discount(self):
        result = self.service.calculate_price(TipoProduto.DIESEL, 600)
        expected = (3.99 * 600) * 0.95
        assert result == expected

    def test_calculate_price_diesel_with_10_percent_discount(self):
        result = self.service.calculate_price(TipoProduto.DIESEL, 1500)
        expected = (3.99 * 1500) * 0.9
        assert result == expected

    def test_calculate_price_diesel_boundary_at_500(self):
        result_at_500 = self.service.calculate_price(TipoProduto.DIESEL, 500)
        expected_at_500 = 3.99 * 500
        assert result_at_500 == expected_at_500

        result_at_501 = self.service.calculate_price(TipoProduto.DIESEL, 501)
        expected_at_501 = (3.99 * 501) * 0.95
        assert result_at_501 == expected_at_501

    def test_calculate_price_diesel_boundary_at_1000(self):
        result_at_1000 = self.service.calculate_price(TipoProduto.DIESEL, 1000)
        expected_at_1000 = (3.99 * 1000) * 0.95
        assert result_at_1000 == expected_at_1000

        result_at_1001 = self.service.calculate_price(TipoProduto.DIESEL, 1001)
        expected_at_1001 = (3.99 * 1001) * 0.9
        assert result_at_1001 == expected_at_1001

    def test_calculate_price_gasolina_no_discount(self):
        result = self.service.calculate_price(TipoProduto.GASOLINA, 100)
        expected = 5.19 * 100
        assert result == expected

    def test_calculate_price_gasolina_with_discount(self):
        result = self.service.calculate_price(TipoProduto.GASOLINA, 250)
        expected = (5.19 * 250) - 100.00
        assert result == expected

    def test_calculate_price_gasolina_boundary_at_200(self):
        result_at_200 = self.service.calculate_price(TipoProduto.GASOLINA, 200)
        expected_at_200 = 5.19 * 200
        assert result_at_200 == expected_at_200

        result_at_201 = self.service.calculate_price(TipoProduto.GASOLINA, 201)
        expected_at_201 = (5.19 * 201) - 100.00
        assert result_at_201 == expected_at_201

    def test_calculate_price_etanol_no_discount(self):
        result = self.service.calculate_price(TipoProduto.ETANOL, 50)
        expected = 3.59 * 50
        assert result == expected

    def test_calculate_price_etanol_with_discount(self):
        result = self.service.calculate_price(TipoProduto.ETANOL, 100)
        expected = (3.59 * 100) * 0.97
        assert result == expected

    def test_calculate_price_etanol_boundary_at_80(self):
        result_at_80 = self.service.calculate_price(TipoProduto.ETANOL, 80)
        expected_at_80 = 3.59 * 80
        assert result_at_80 == expected_at_80

        result_at_81 = self.service.calculate_price(TipoProduto.ETANOL, 81)
        expected_at_81 = (3.59 * 81) * 0.97
        assert result_at_81 == expected_at_81

    def test_calculate_price_lubrificante_no_discount(self):
        result = self.service.calculate_price(TipoProduto.LUBRIFICANTE, 10)
        expected = 25.00 * 10
        assert result == expected

    def test_calculate_price_lubrificante_large_quantity(self):
        result = self.service.calculate_price(TipoProduto.LUBRIFICANTE, 1000)
        expected = 25.00 * 1000
        assert result == expected

    def test_calculate_price_with_zero_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            self.service.calculate_price(TipoProduto.DIESEL, 0)

    def test_calculate_price_with_negative_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            self.service.calculate_price(TipoProduto.DIESEL, -5)

    def test_calculate_price_with_quantity_one(self):
        result = self.service.calculate_price(TipoProduto.DIESEL, 1)
        expected = 3.99
        assert result == expected

    @pytest.mark.parametrize("tipo_produto,quantidade,expected", [
        (TipoProduto.DIESEL, 100, 3.99 * 100),
        (TipoProduto.DIESEL, 501, (3.99 * 501) * 0.95),
        (TipoProduto.DIESEL, 1001, (3.99 * 1001) * 0.9),
        (TipoProduto.GASOLINA, 100, 5.19 * 100),
        (TipoProduto.GASOLINA, 201, (5.19 * 201) - 100.00),
        (TipoProduto.ETANOL, 50, 3.59 * 50),
        (TipoProduto.ETANOL, 81, (3.59 * 81) * 0.97),
        (TipoProduto.LUBRIFICANTE, 10, 25.00 * 10),
    ])
    def test_calculate_price_parametrized(self, tipo_produto, quantidade, expected):
        result = self.service.calculate_price(tipo_produto, quantidade)
        assert result == expected
