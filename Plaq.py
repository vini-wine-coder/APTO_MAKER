class Plaq:
    def __init__(self, nome, indice):
        self.nome = nome
        self.indice = indice

    def __repr__(self):
        return f"Plaq(nome='{self.nome}', indice={self.indice})"
