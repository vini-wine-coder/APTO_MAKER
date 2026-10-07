import math

LARGURA_FRAME = 620
ALTURA_FRAME = 550


def por_linha_max(largura_rect=50, largura_frame=LARGURA_FRAME):
    return largura_frame // largura_rect


def gerar_linhas(obj_sequenc, passes, largura_frame=LARGURA_FRAME):
    """
    Gera a sequência de LINHAS (não de folhas) na ordem certa:
    primeiro TODAS as linhas da passada 1, depois TODAS da passada 2,
    depois TODAS da passada 3 — não mistura passadas por item.

    `passes` é uma lista de (largura_rect, altura_rect), uma por passada.
    Cada linha é um dict: {"itens": [...], "largura": .., "altura": ..}
    """
    linhas = []
    for largura_rect, altura_rect in passes:
        por_linha = por_linha_max(largura_rect, largura_frame)
        for i in range(0, len(obj_sequenc), por_linha):
            itens = obj_sequenc[i:i + por_linha]
            linhas.append({"itens": itens, "largura": largura_rect, "altura": altura_rect})
    return linhas


def distribuir_em_folhas(linhas, altura_disponivel):
    """
    Distribui as linhas (já geradas por gerar_linhas) em folhas,
    empilhando até estourar o orçamento de altura por folha.
    Continua o fluxo — não reinicia a cada passada nem a cada item.

    Retorna uma lista de folhas; cada folha é uma lista de
    (linha, y_local) — y_local é o y (de baixo pra cima) dentro da folha.
    """
    folhas = []
    folha_atual = []
    altura_usada = 0

    for linha in linhas:
        if altura_usada + linha["altura"] > altura_disponivel:
            folhas.append(folha_atual)
            folha_atual = []
            altura_usada = 0
        folha_atual.append((linha, altura_usada))
        altura_usada += linha["altura"]

    if folha_atual:
        folhas.append(folha_atual)

    return folhas
