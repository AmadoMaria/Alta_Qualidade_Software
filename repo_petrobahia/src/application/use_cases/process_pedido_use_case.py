from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto
from domain.services.discount_service import DiscountService
from domain.services.pricing_service import PricingService
from domain.services.rounding_service import RoundingService
from ports.cliente_repository_port import ClienteRepositoryPort
from ports.pedido_repository_port import PedidoRepositoryPort


@dataclass
class ProcessPedidoRequest:
    id: str
    cliente_id: str
    tipo_produto: str
    quantidade: int
    cupom: Optional[str] = None


@dataclass
class ProcessPedidoResponse:
    success: bool
    message: str
    total: Optional[Decimal] = None
    pedido: Optional[Pedido] = None


class ProcessPedidoUseCase:
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

    def execute(self, request: ProcessPedidoRequest) -> ProcessPedidoResponse:
        cliente = self._cliente_repository.find_by_id(request.cliente_id)
        if not cliente:
            return ProcessPedidoResponse(
                success=False,
                message=f"Customer not found: {request.cliente_id}",
            )

        try:
            tipo_produto = TipoProduto(request.tipo_produto)
        except ValueError:
            return ProcessPedidoResponse(
                success=False,
                message=f"Invalid product type: {request.tipo_produto}",
            )

        if request.quantidade <= 0:
            return ProcessPedidoResponse(
                success=False,
                message="Quantity must be positive",
            )

        try:
            pedido = Pedido(
                id=request.id,
                cliente_id=request.cliente_id,
                tipo_produto=tipo_produto,
                quantidade=request.quantidade,
                cupom=request.cupom,
            )
        except ValueError as e:
            return ProcessPedidoResponse(
                success=False,
                message=str(e),
            )

        price = self._pricing_service.calculate_price(
            tipo_produto, request.quantidade
        )

        price = self._discount_service.apply_coupon(
            price, request.cupom, tipo_produto
        )

        final_price = self._rounding_service.round_price(price, tipo_produto)

        if not self._pedido_repository.save(pedido):
            return ProcessPedidoResponse(
                success=False,
                message="Failed to save order",
            )

        return ProcessPedidoResponse(
            success=True,
            message="Order processed successfully",
            total=final_price,
            pedido=pedido,
        )
