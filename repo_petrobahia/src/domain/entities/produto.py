from dataclasses import dataclass
from enum import Enum


class TipoProduto(Enum):
    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    LUBRIFICANTE = "lubrificante"


@dataclass(frozen=True)
class Produto:
    tipo: TipoProduto
    preco_base: float

    def __post_init__(self) -> None:
        if self.preco_base < 0:
            raise ValueError("Product base price cannot be negative")
