import pytest
from domain.services.discount_service import DiscountService
from domain.entities.produto import TipoProduto


class TestDiscountService:

    def setup_method(self):
        self.service = DiscountService()

    def test_apply_coupon_with_no_coupon_returns_original_price(self):
        result = self.service.apply_coupon(1000.0, None, TipoProduto.DIESEL)
        assert result == 1000.0

    def test_apply_coupon_with_empty_string_returns_original_price(self):
        result = self.service.apply_coupon(1000.0, "", TipoProduto.DIESEL)
        assert result == 1000.0

    def test_apply_coupon_mega10_percentual_discount(self):
        result = self.service.apply_coupon(1000.0, "MEGA10", TipoProduto.DIESEL)
        expected = 1000.0 * 0.9
        assert result == expected

    def test_apply_coupon_novo5_percentual_discount(self):
        result = self.service.apply_coupon(1000.0, "NOVO5", TipoProduto.GASOLINA)
        expected = 1000.0 * 0.95
        assert result == expected

    def test_apply_coupon_lub2_fixo_discount(self):
        result = self.service.apply_coupon(100.0, "LUB2", TipoProduto.LUBRIFICANTE)
        expected = 100.0 - 2.0
        assert result == expected

    def test_apply_coupon_case_insensitive_lowercase(self):
        result = self.service.apply_coupon(1000.0, "mega10", TipoProduto.DIESEL)
        expected = 1000.0 * 0.9
        assert result == expected

    def test_apply_coupon_case_insensitive_mixed_case(self):
        result = self.service.apply_coupon(1000.0, "MeGa10", TipoProduto.DIESEL)
        expected = 1000.0 * 0.9
        assert result == expected

    def test_apply_coupon_invalid_coupon_returns_original_price(self):
        result = self.service.apply_coupon(1000.0, "INVALID", TipoProduto.DIESEL)
        assert result == 1000.0

    def test_apply_coupon_lub2_restricted_to_lubrificante(self):
        result_lubrificante = self.service.apply_coupon(100.0, "LUB2", TipoProduto.LUBRIFICANTE)
        assert result_lubrificante == 98.0

        result_diesel = self.service.apply_coupon(100.0, "LUB2", TipoProduto.DIESEL)
        assert result_diesel == 100.0

    def test_apply_coupon_lub2_not_applicable_to_diesel(self):
        result = self.service.apply_coupon(1000.0, "LUB2", TipoProduto.DIESEL)
        assert result == 1000.0

    def test_apply_coupon_lub2_not_applicable_to_gasolina(self):
        result = self.service.apply_coupon(1000.0, "LUB2", TipoProduto.GASOLINA)
        assert result == 1000.0

    def test_apply_coupon_lub2_not_applicable_to_etanol(self):
        result = self.service.apply_coupon(1000.0, "LUB2", TipoProduto.ETANOL)
        assert result == 1000.0

    def test_apply_coupon_mega10_applicable_to_all_products(self):
        for tipo_produto in TipoProduto:
            result = self.service.apply_coupon(1000.0, "MEGA10", tipo_produto)
            expected = 1000.0 * 0.9
            assert result == expected

    def test_apply_coupon_novo5_applicable_to_all_products(self):
        for tipo_produto in TipoProduto:
            result = self.service.apply_coupon(1000.0, "NOVO5", tipo_produto)
            expected = 1000.0 * 0.95
            assert result == expected

    def test_apply_coupon_with_small_price(self):
        result = self.service.apply_coupon(10.0, "MEGA10", TipoProduto.DIESEL)
        expected = 10.0 * 0.9
        assert result == expected

    def test_apply_coupon_with_large_price(self):
        result = self.service.apply_coupon(100000.0, "MEGA10", TipoProduto.DIESEL)
        expected = 100000.0 * 0.9
        assert result == expected

    def test_apply_coupon_mega10_reduces_price_by_10_percent(self):
        original = 1000.0
        result = self.service.apply_coupon(original, "MEGA10", TipoProduto.DIESEL)
        discount = original - result
        assert discount == 100.0

    def test_apply_coupon_novo5_reduces_price_by_5_percent(self):
        original = 1000.0
        result = self.service.apply_coupon(original, "NOVO5", TipoProduto.GASOLINA)
        discount = original - result
        assert discount == 50.0

    def test_apply_coupon_lub2_reduces_price_by_2_reais(self):
        original = 100.0
        result = self.service.apply_coupon(original, "LUB2", TipoProduto.LUBRIFICANTE)
        discount = original - result
        assert discount == 2.0

    @pytest.mark.parametrize("coupon_code,expected_discount_multiplier", [
        ("MEGA10", 0.9),
        ("mega10", 0.9),
        ("MEGA10", 0.9),
        ("MeGa10", 0.9),
    ])
    def test_apply_coupon_mega10_case_variations(self, coupon_code, expected_discount_multiplier):
        result = self.service.apply_coupon(1000.0, coupon_code, TipoProduto.DIESEL)
        expected = 1000.0 * expected_discount_multiplier
        assert result == expected

    @pytest.mark.parametrize("tipo_produto", [
        TipoProduto.DIESEL,
        TipoProduto.GASOLINA,
        TipoProduto.ETANOL,
        TipoProduto.LUBRIFICANTE,
    ])
    def test_apply_coupon_mega10_all_products(self, tipo_produto):
        result = self.service.apply_coupon(1000.0, "MEGA10", tipo_produto)
        assert result == 900.0

    @pytest.mark.parametrize("invalid_code", [
        "INVALID",
        "NOTEXIST",
        "12345",
        "MEGA",
        "MEGA11",
    ])
    def test_apply_coupon_invalid_codes(self, invalid_code):
        result = self.service.apply_coupon(1000.0, invalid_code, TipoProduto.DIESEL)
        assert result == 1000.0

    def test_apply_coupon_with_zero_price(self):
        result = self.service.apply_coupon(0.0, "MEGA10", TipoProduto.DIESEL)
        assert result == 0.0

    def test_apply_coupon_lub2_with_price_lower_than_discount(self):
        result = self.service.apply_coupon(1.0, "LUB2", TipoProduto.LUBRIFICANTE)
        expected = 1.0 - 2.0
        assert result == expected
