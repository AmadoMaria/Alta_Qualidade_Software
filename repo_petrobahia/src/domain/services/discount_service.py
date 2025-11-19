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

        for cupom_enum in Cupom:
            cupom_data = cupom_enum.value
            if cupom_data.codigo == cupom_upper:
                if cupom_data.produto_restrito and cupom_data.produto_restrito != tipo_produto:
                    return price

                if cupom_data.tipo_desconto == "percentual":
                    return price * (1 - cupom_data.valor_desconto)
                elif cupom_data.tipo_desconto == "fixo":
                    return price - cupom_data.valor_desconto

        return price
