import json
from pathlib import Path
from typing import List, Optional

from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto
from ports.pedido_repository_port import PedidoRepositoryPort


class JsonPedidoRepository(PedidoRepositoryPort):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.file_path = self.data_dir / "pedidos.json"
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

    def save(self, pedido: Pedido) -> bool:
        pedidos = self._read_data()

        if any(p.get("id") == pedido.id for p in pedidos):
            return False

        pedido_dict = {
            "id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "tipo_produto": pedido.tipo_produto.value,
            "quantidade": pedido.quantidade,
            "cupom": pedido.cupom,
        }

        pedidos.append(pedido_dict)
        return self._write_data(pedidos)

    def find_by_id(self, pedido_id: str) -> Optional[Pedido]:
        pedidos = self._read_data()
        for p in pedidos:
            if p.get("id") == pedido_id:
                return Pedido(
                    id=p["id"],
                    cliente_id=p["cliente_id"],
                    tipo_produto=TipoProduto(p["tipo_produto"]),
                    quantidade=p["quantidade"],
                    cupom=p.get("cupom"),
                )
        return None

    def find_by_cliente_id(self, cliente_id: str) -> List[Pedido]:
        pedidos = self._read_data()
        result = []
        for p in pedidos:
            if p.get("cliente_id") == cliente_id:
                result.append(
                    Pedido(
                        id=p["id"],
                        cliente_id=p["cliente_id"],
                        tipo_produto=TipoProduto(p["tipo_produto"]),
                        quantidade=p["quantidade"],
                        cupom=p.get("cupom"),
                    )
                )
        return result
