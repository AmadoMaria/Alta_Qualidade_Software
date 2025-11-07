from decimal import Decimal

from domain.entities.produto import TipoProduto


class PricingService:
    _BASE_PRICES = {
        TipoProduto.DIESEL: Decimal("3.99"),
        TipoProduto.GASOLINA: Decimal("5.19"),
        TipoProduto.ETANOL: Decimal("3.59"),
        TipoProduto.LUBRIFICANTE: Decimal("25.00"),
    }

    def calculate_price(
        self, tipo_produto: TipoProduto, quantidade: int
    ) -> Decimal:
        if quantidade <= 0:
            raise ValueError("Quantity must be positive")

        base_price = self._BASE_PRICES.get(tipo_produto)
        if not base_price:
            raise ValueError(f"Unknown product type: {tipo_produto}")

        total = base_price * quantidade

        if tipo_produto == TipoProduto.DIESEL:
            return self._apply_diesel_discount(total, quantidade)
        elif tipo_produto == TipoProduto.GASOLINA:
            return self._apply_gasolina_discount(total, quantidade)
        elif tipo_produto == TipoProduto.ETANOL:
            return self._apply_etanol_discount(total, quantidade)

        return total

    def _apply_diesel_discount(
        self, total: Decimal, quantidade: int
    ) -> Decimal:
        if quantidade > 1000:
            return total * Decimal("0.90")
        elif quantidade > 500:
            return total * Decimal("0.95")
        return total

    def _apply_gasolina_discount(
        self, total: Decimal, quantidade: int
    ) -> Decimal:
        if quantidade > 200:
            return total - Decimal("100.00")
        return total

    def _apply_etanol_discount(
        self, total: Decimal, quantidade: int
    ) -> Decimal:
        if quantidade > 80:
            return total * Decimal("0.97")
        return total
