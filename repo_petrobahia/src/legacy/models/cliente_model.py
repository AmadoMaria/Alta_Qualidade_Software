class Cliente:
    def __init__(self, id_cliente, nome_cliente, email_cliente, cnpj_cliente):
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.email_cliente = email_cliente
        self.cnpj_cliente = cnpj_cliente
        self.pedidos = []

