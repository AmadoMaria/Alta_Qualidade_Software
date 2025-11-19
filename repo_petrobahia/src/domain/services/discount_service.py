from typing import Optional

from domain.entities.cupom import Cupom
from domain.entities.produto import TipoProduto


class DiscountService:
    def apply_coupon(
        self,
        price: float,
        cupom: Optional[str],
        tipo_produto: TipoProduto,
    ) -> float:
        if not cupom:
            return price

        cupom_upper = cupom.upper()

        if cupom_upper == Cupom.MEGA10.value:
            return price * 0.9
        elif cupom_upper == Cupom.NOVO5.value:
            return price * 0.95
        elif cupom_upper == Cupom.LUB2.value and tipo_produto == TipoProduto.LUBRIFICANTE:
            return price - 2.00

        return price
