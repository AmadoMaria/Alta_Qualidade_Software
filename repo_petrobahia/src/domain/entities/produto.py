from enum import Enum

from pydantic import BaseModel, field_validator


class TipoProduto(Enum):
    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    LUBRIFICANTE = "lubrificante"


class Produto(BaseModel):
    tipo: TipoProduto
    preco_base: float

    model_config = {
        "frozen": True,
    }

    @field_validator("preco_base")
    def validar_preco_base(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Product base price cannot be negative")
        return value
