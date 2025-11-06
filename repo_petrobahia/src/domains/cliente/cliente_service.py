import re

REG_EMAIL = "^[^@\s]+@[^@\s]+\.[^@\s]+$"

class ClienteService:

    def __init__(self):
        return

    def cadastrar_cliente(self, c):
        if "email" not in c or "nome" not in c:
            print("faltou campo")
            return False
        if not re.match(REG_EMAIL, c["email"]):
            print("email invalido mas vou aceitar assim mesmo")
        f = open("clientes.txt", "a", encoding="utf-8")
        f.write(str(c) + "\n")
        f.close()
        print("enviando email de boas vindas para", c["email"])
        return True

    def cadastrar_clientes(self, clientes):
        for c in clientes:
            ok = self.cadastrar_cliente(c)
            if ok:
                print("cliente ok:", c["nome"])
            else:
                print("cliente com problema:", c)