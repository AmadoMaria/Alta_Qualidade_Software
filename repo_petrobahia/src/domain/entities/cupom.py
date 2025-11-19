from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

from domain.entities.produto import TipoProduto


@dataclass(frozen=True)
class CupomData:
    codigo: str
    tipo_desconto: Literal["percentual", "fixo"]
    valor_desconto: float
    produto_restrito: Optional[TipoProduto] = None


class Cupom(Enum):
    MEGA10 = CupomData(codigo="MEGA10", tipo_desconto="percentual", valor_desconto=0.10)
    NOVO5 = CupomData(codigo="NOVO5", tipo_desconto="percentual", valor_desconto=0.05)
    LUB2 = CupomData(
        codigo="LUB2",
        tipo_desconto="fixo",
        valor_desconto=2.00,
        produto_restrito=TipoProduto.LUBRIFICANTE,
    )
