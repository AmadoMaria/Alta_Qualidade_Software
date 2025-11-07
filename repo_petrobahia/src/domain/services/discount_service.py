from decimal import Decimal
from typing import Optional

from domain.entities.produto import TipoProduto


class DiscountService:
    def apply_coupon(
        self,
        price: Decimal,
        cupom: Optional[str],
        tipo_produto: TipoProduto,
    ) -> Decimal:
        if not cupom:
            return price

        cupom_upper = cupom.upper()

        if cupom_upper == "MEGA10":
            return price * Decimal("0.90")
        elif cupom_upper == "NOVO5":
            return price * Decimal("0.95")
        elif cupom_upper == "LUB2" and tipo_produto == TipoProduto.LUBRIFICANTE:
            return price - Decimal("2.00")

        return price
