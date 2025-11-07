import json
from pathlib import Path
from typing import List, Optional

from domain.entities.cliente import Cliente
from ports.cliente_repository_port import ClienteRepositoryPort


class JsonClienteRepository(ClienteRepositoryPort):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.file_path = self.data_dir / "clientes.json"
        self._ensure_setup()

    def _ensure_setup(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_data([])

    def _read_data(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[dict]) -> bool:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def save(self, cliente: Cliente) -> bool:
        clientes = self._read_data()

        if any(c.get("id") == cliente.id for c in clientes):
            return False

        cliente_dict = {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "cnpj": cliente.cnpj,
        }

        clientes.append(cliente_dict)
        return self._write_data(clientes)

    def find_by_id(self, cliente_id: str) -> Optional[Cliente]:
        clientes = self._read_data()
        for c in clientes:
            if c.get("id") == cliente_id:
                return Cliente(
                    id=c["id"],
                    nome=c["nome"],
                    email=c["email"],
                    cnpj=c["cnpj"],
                )
        return None

    def find_by_email(self, email: str) -> Optional[Cliente]:
        clientes = self._read_data()
        for c in clientes:
            if c.get("email") == email:
                return Cliente(
                    id=c["id"],
                    nome=c["nome"],
                    email=c["email"],
                    cnpj=c["cnpj"],
                )
        return None

    def exists_by_email(self, email: str) -> bool:
        clientes = self._read_data()
        return any(c.get("email") == email for c in clientes)
