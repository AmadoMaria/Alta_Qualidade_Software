from domain.entities.produto import TipoProduto


class RoundingService:
    def round_price(self, price: float, tipo_produto: TipoProduto) -> float:
        if tipo_produto == TipoProduto.DIESEL:
            return round(price, 0)

        return round(price, 2)
