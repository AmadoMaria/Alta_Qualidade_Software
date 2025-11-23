import pytest
from unittest.mock import Mock
from domain.services.client_service import ClientService
from domain.entities.cliente import Cliente


class TestClientService:

    def setup_method(self):
        self.mock_repository = Mock()
        self.mock_notification = Mock()
        self.service = ClientService(self.mock_repository, self.mock_notification)

    def test_register_client_successful(self):
        self.mock_repository.save.return_value = True

        cliente = self.service.register_client(
            name="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        assert cliente.nome == "Empresa Teste"
        assert cliente.email == "contato@empresa.com"
        assert cliente.cnpj == "12345678901234"
        assert cliente.id is not None

    def test_register_client_calls_repository_save(self):
        self.mock_repository.save.return_value = True

        self.service.register_client(
            name="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        self.mock_repository.save.assert_called_once()
        saved_cliente = self.mock_repository.save.call_args[0][0]
        assert isinstance(saved_cliente, Cliente)

    def test_register_client_sends_welcome_email(self):
        self.mock_repository.save.return_value = True

        cliente = self.service.register_client(
            name="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        self.mock_notification.send_welcome_email.assert_called_once_with(cliente)

    def test_register_client_raises_exception_on_save_failure(self):
        self.mock_repository.save.return_value = False

        with pytest.raises(Exception, match="Failed to save client"):
            self.service.register_client(
                name="Empresa Teste",
                email="contato@empresa.com",
                cnpj="12345678901234"
            )

    def test_register_client_does_not_send_email_on_save_failure(self):
        self.mock_repository.save.return_value = False

        with pytest.raises(Exception):
            self.service.register_client(
                name="Empresa Teste",
                email="contato@empresa.com",
                cnpj="12345678901234"
            )

        self.mock_notification.send_welcome_email.assert_not_called()

    def test_register_client_validates_email(self):
        self.mock_repository.save.return_value = True

        with pytest.raises(ValueError, match="Invalid email format"):
            self.service.register_client(
                name="Empresa Teste",
                email="invalid-email",
                cnpj="12345678901234"
            )

    def test_register_client_validates_cnpj(self):
        self.mock_repository.save.return_value = True

        with pytest.raises(ValueError, match="CNPJ deve conter 14 dígitos"):
            self.service.register_client(
                name="Empresa Teste",
                email="contato@empresa.com",
                cnpj="123"
            )

    def test_register_client_accepts_formatted_cnpj(self):
        self.mock_repository.save.return_value = True

        cliente = self.service.register_client(
            name="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12.345.678/9012-34"
        )

        assert cliente.cnpj == "12345678901234"

    def test_register_client_strips_whitespace_from_name(self):
        self.mock_repository.save.return_value = True

        cliente = self.service.register_client(
            name="  Empresa Teste  ",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        assert cliente.nome == "Empresa Teste"

    def test_register_client_strips_whitespace_from_email(self):
        self.mock_repository.save.return_value = True

        cliente = self.service.register_client(
            name="Empresa Teste",
            email="  contato@empresa.com  ",
            cnpj="12345678901234"
        )

        assert cliente.email == "contato@empresa.com"

    def test_register_client_returns_cliente_instance(self):
        self.mock_repository.save.return_value = True

        result = self.service.register_client(
            name="Empresa Teste",
            email="contato@empresa.com",
            cnpj="12345678901234"
        )

        assert isinstance(result, Cliente)

    def test_register_client_generates_unique_id(self):
        self.mock_repository.save.return_value = True

        cliente1 = self.service.register_client(
            name="Empresa 1",
            email="empresa1@test.com",
            cnpj="12345678901234"
        )

        cliente2 = self.service.register_client(
            name="Empresa 2",
            email="empresa2@test.com",
            cnpj="98765432109876"
        )

        assert cliente1.id != cliente2.id

    def test_register_client_with_valid_email_formats(self):
        self.mock_repository.save.return_value = True

        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
        ]

        for email in valid_emails:
            cliente = self.service.register_client(
                name="Empresa",
                email=email,
                cnpj="12345678901234"
            )
            assert cliente.email == email

    @pytest.mark.parametrize("invalid_email", [
        "plaintext",
        "@example.com",
        "user@",
        "user name@example.com",
    ])
    def test_register_client_rejects_invalid_emails(self, invalid_email):
        self.mock_repository.save.return_value = True

        with pytest.raises(ValueError):
            self.service.register_client(
                name="Empresa",
                email=invalid_email,
                cnpj="12345678901234"
            )
