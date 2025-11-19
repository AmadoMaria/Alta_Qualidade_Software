from typing import Optional

from pydantic import BaseModel, Field, field_validator

from domain.entities.produto import TipoProduto


class Pedido(BaseModel):
    id: str
    cliente_id: str
    tipo_produto: TipoProduto
    quantidade: int
    cupom: Optional[str] = None

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }

    @field_validator("id")
    def validar_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Order ID cannot be empty")
        return value

    @field_validator("cliente_id")
    def validar_cliente_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Customer ID cannot be empty")
        return value

    @field_validator("quantidade")
    def validar_quantidade(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Order quantity must be positive")
        return value
