from typing import Optional

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

        if cupom_upper == "MEGA10":
            return price * 0.9
        elif cupom_upper == "NOVO5":
            return price * 0.95
        elif cupom_upper == "LUB2" and tipo_produto == TipoProduto.LUBRIFICANTE:
            return price - 2.00

        return price
