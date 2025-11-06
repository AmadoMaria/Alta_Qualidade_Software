from legacy.pedido_service import processar_pedido
from legacy.clientes import cadastrar_cliente

pedidos = [
    {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
    {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
    {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
    {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
]

clientes = [
    {"nome": "Ana Paula", "email": "ana@@petrobahia", "cnpj": "123"},
    {"nome": "Carlos", "email": "carlos@petrobahia.com", "cnpj": "456"},
]

if __name__ == "__main__":
    
    print("==== Início processamento PetroBahia ====")

# for c in clientes:
#     ok = cadastrar_cliente(c)
#     if ok:
#         print("cliente ok:", c["nome"])
#     else:
#         print("cliente com problema:", c)
 

# for p in pedidos:
#     v = processar_pedido(p)
#     valores.append(v)
#     print("pedido:", p, "-- valor final:", v)

# return valores = []

# print("TOTAL =", sum(valores))
# print("==== Fim processamento PetroBahia ====")
