from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto
from domain.services.discount_service import DiscountService
from domain.services.pricing_service import PricingService
from domain.services.rounding_service import RoundingService
from ports.cliente_repository_port import ClienteRepositoryPort
from ports.pedido_repository_port import PedidoRepositoryPort


class PedidoService:
    def __init__(
        self,
        pedido_repository: PedidoRepositoryPort,
        cliente_repository: ClienteRepositoryPort,
    ):
        self._pedido_repository = pedido_repository
        self._cliente_repository = cliente_repository
        self._pricing_service = PricingService()
        self._discount_service = DiscountService()
        self._rounding_service = RoundingService()

    def process_pedido(
        self,
        id: str,
        cliente_id: str,
        tipo_produto: TipoProduto,
        quantidade: int,
        cupom: str = None,
    ) -> tuple[Pedido, float]:
        cliente = self._cliente_repository.find_by_id(cliente_id)
        if not cliente:
            raise ValueError(f"Customer not found: {cliente_id}")

        if quantidade <= 0:
            raise ValueError("Quantity must be positive")

        pedido = Pedido(
            id=id,
            cliente_id=cliente_id,
            tipo_produto=tipo_produto,
            quantidade=quantidade,
            cupom=cupom,
        )

        price = self._pricing_service.calculate_price(tipo_produto, quantidade)
        price = self._discount_service.apply_coupon(price, cupom, tipo_produto)
        final_price = self._rounding_service.round_price(price, tipo_produto)

        if not self._pedido_repository.save(pedido):
            raise Exception("Failed to save order")

        return pedido, final_price
