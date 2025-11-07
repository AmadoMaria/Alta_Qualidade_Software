class Produto:

    def __init__(self, id_produto, tipo, preco):
        self.id_produto = id_produto
        self.tipo = tipo
        self.preco = preco
        self.pedidos = []
        