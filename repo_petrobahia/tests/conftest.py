import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
src_path = repo_root / "src"
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import Mock
from domain.entities.cliente import Cliente
from domain.entities.pedido import Pedido
from domain.entities.produto import TipoProduto, Produto
from domain.entities.cupom import Cupom


@pytest.fixture
def valid_cliente():
    return Cliente(
        id="test-client-123",
        nome="Empresa Teste Ltda",
        email="contato@empresa.com",
        cnpj="12345678901234"
    )


@pytest.fixture
def valid_pedido():
    return Pedido(
        id="pedido-001",
        cliente_id="test-client-123",
        tipo_produto=TipoProduto.DIESEL,
        quantidade=100,
        cupom=None
    )


@pytest.fixture
def produto_diesel():
    return Produto(tipo=TipoProduto.DIESEL, preco_base=5.50)


@pytest.fixture
def produto_gasolina():
    return Produto(tipo=TipoProduto.GASOLINA, preco_base=6.00)


@pytest.fixture
def produto_etanol():
    return Produto(tipo=TipoProduto.ETANOL, preco_base=4.50)


@pytest.fixture
def produto_lubrificante():
    return Produto(tipo=TipoProduto.LUBRIFICANTE, preco_base=25.00)


@pytest.fixture
def mock_cliente_repository():
    repository = Mock()
    repository.save.return_value = None
    repository.find_by_id.return_value = None
    repository.find_by_email.return_value = None
    repository.exists_by_email.return_value = False
    return repository


@pytest.fixture
def mock_pedido_repository():
    repository = Mock()
    repository.save.return_value = None
    repository.find_by_id.return_value = None
    repository.find_by_cliente_id.return_value = []
    return repository


@pytest.fixture
def mock_notification_service():
    service = Mock()
    service.send_welcome_email.return_value = None
    service.send_order_confirmation.return_value = None
    return service
