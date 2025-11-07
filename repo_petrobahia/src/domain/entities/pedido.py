from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from domain.entities.produto import TipoProduto


@dataclass(frozen=True)
class Pedido:
    id: str
    cliente_id: str
    tipo_produto: TipoProduto
    quantidade: int
    cupom: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Order ID cannot be empty")
        if not self.cliente_id:
            raise ValueError("Customer ID cannot be empty")
        if self.quantidade <= 0:
            raise ValueError("Order quantity must be positive")
