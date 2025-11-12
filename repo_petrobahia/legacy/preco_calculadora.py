BASES = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
}


def calcular_preco(tipo, qtd):
    if tipo == "diesel":
        if qtd > 1000:
            preco = (BASES["diesel"] * qtd) * 0.9
        else:
            if qtd > 500:
                preco = (BASES["diesel"] * qtd) * 0.95
            else:
                preco = BASES["diesel"] * qtd
        print("calc diesel", preco)
        return preco
    else:
        if tipo == "gasolina":
            if qtd > 200:
                preco = (BASES["gasolina"] * qtd) - 100
            else:
                preco = BASES["gasolina"] * qtd
            print("calc gas", preco)
            return preco
        else:
            if tipo == "etanol":
                preco = BASES["etanol"] * qtd
                if qtd > 80:
                    preco = preco * 0.97
                print("calc eta", preco)
                return preco
            else:
                if tipo == "lubrificante":
                    x = 0
                    for i in range(qtd):
                        x = x + BASES["lubrificante"]
                    return x
                else:
                    print("tipo desconhecido, devolvendo 0")
                    return 0
