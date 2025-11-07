from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Cliente:
    id: str
    nome: str
    email: str
    cnpj: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Cliente ID cannot be empty")
        if not self.nome:
            raise ValueError("Cliente name cannot be empty")
        if not self.email:
            raise ValueError("Cliente email cannot be empty")
        if not self.cnpj:
            raise ValueError("Cliente CNPJ cannot be empty")
