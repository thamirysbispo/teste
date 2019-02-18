

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


class Produto:
    def __init__(self, nome, categoria, valor, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.valor = valor