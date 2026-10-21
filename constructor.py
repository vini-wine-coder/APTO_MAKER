from Plaq import Plaq


def plano(lines):
    """
    Uma placa por linha: cada linha nao vazia (sem espacos nas pontas) vira
    um Plaq com aquele texto. Aceita qualquer texto, nao so "APTO 101".
    Linhas vazias sao ignoradas.
    """
    textos = [linha.strip() for linha in lines]
    textos = [texto for texto in textos if texto]
    return [Plaq(texto, idx) for idx, texto in enumerate(textos)]
