from dataclasses import dataclass
from typing import Optional

from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto
from domain.services.pedido_service import PedidoService
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
    total: Optional[float] = None
    pedido: Optional[Pedido] = None


class ProcessPedidoUseCase:
    def __init__(
        self,
        pedido_repository: PedidoRepositoryPort,
        cliente_repository: ClienteRepositoryPort,
    ):
        self._pedido_service = PedidoService(pedido_repository, cliente_repository)

    def execute(self, request: ProcessPedidoRequest) -> ProcessPedidoResponse:
        try:
            tipo_produto = TipoProduto(request.tipo_produto)
        except ValueError:
            return ProcessPedidoResponse(
                success=False,
                message=f"Invalid product type: {request.tipo_produto}",
            )

        try:
            pedido, final_price = self._pedido_service.process_pedido(
                request.id,
                request.cliente_id,
                tipo_produto,
                request.quantidade,
                request.cupom,
            )
            return ProcessPedidoResponse(
                success=True,
                message="Order processed successfully",
                total=final_price,
                pedido=pedido,
            )
        except ValueError as e:
            return ProcessPedidoResponse(
                success=False,
                message=str(e),
            )
        except Exception as e:
            return ProcessPedidoResponse(
                success=False,
                message="Failed to process order",
            )
