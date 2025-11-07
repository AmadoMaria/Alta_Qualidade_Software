from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from domain.entities.produto import TipoProduto


class RoundingService:
    def round_price(self, price: Decimal, tipo_produto: TipoProduto) -> Decimal:
        if tipo_produto == TipoProduto.DIESEL:
            return price.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        elif tipo_produto == TipoProduto.GASOLINA:
            return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return price.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
