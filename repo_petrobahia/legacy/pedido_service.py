from legacy.preco_calculadora import calcular_preco

def processar_pedido(p):
    prod = p.get("produto")
    qtd = p.get("qtd")
    cupom = p.get("cupom")

    if qtd == 0:
        print("qtd zero, retornando 0")
        return 0

    preco = calcular_preco(prod, qtd)
    if preco < 0:
        print("algo deu errado, preco negativo")
        preco = 0

    if cupom == "MEGA10": #Não respeita o SOLID -> Lógica de cupons + seleção de produto +
        preco = preco - (preco * 0.1)
    else:
        if cupom == "NOVO5":
            preco = preco - (preco * 0.05)
        else:
            if cupom == "LUB2" and prod == "lubrificante":
                preco = preco - 2
            else:
                preco = preco

    if prod == "diesel":
        preco = round(preco, 0)
    else:
        if prod == "gasolina":
            preco = round(preco, 2)
        else:
            preco = float(int(preco * 100) / 100.0)

    print("pedido ok:", p["cliente"], prod, qtd, "=>", preco)
    return preco
