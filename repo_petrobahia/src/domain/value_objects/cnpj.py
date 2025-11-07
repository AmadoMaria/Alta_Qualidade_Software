import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CNPJ:
    value: str

    CNPJ_PATTERN = re.compile(r"^\d{14}$")

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("CNPJ cannot be empty")

        clean_cnpj = re.sub(r"[^\d]", "", self.value)

        if not self.CNPJ_PATTERN.match(clean_cnpj):
            raise ValueError(
                f"Invalid CNPJ format: {self.value}. Must contain 14 digits"
            )

        object.__setattr__(self, "value", clean_cnpj)

    def __str__(self) -> str:
        return self.value

    def formatted(self) -> str:
        v = self.value
        return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"
