class Pedido:

    def __init__(
        self,
        id_pedido: str,
        quantidade: int,
        cupom: str,
        valor_total: float,
        cliente: str,
    ):
        self.id_pedido = id_pedido
        self.quantidade = quantidade
        self.cupom = cupom
        self.valor_total = valor_total
        self.cliente = cliente
        self.produtos = []
