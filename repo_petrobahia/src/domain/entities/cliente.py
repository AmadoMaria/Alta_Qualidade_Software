import re
from typing import ClassVar
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class Cliente(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    nome: str
    email: str
    cnpj: str

    EMAIL_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }

    @field_validator("cnpj")
    def validar_cnpj(cls, value: str) -> str:
        cnpj = "".join(filter(str.isdigit, value))
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")
        return cnpj

    @field_validator("email")
    def validar_email(cls, value: str) -> str:
        if not value:
            raise ValueError("Email cannot be empty")
        if not cls.EMAIL_PATTERN.match(value):
            raise ValueError(f"Invalid email format: {value}")
        return value
