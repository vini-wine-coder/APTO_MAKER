import math

LARGURA_FRAME = 620
ALTURA_FRAME = 550


def por_linha_max(largura_rect=50, largura_frame=LARGURA_FRAME):
    """Quantos retângulos cabem lado a lado sem estourar o frame."""
    return largura_frame // largura_rect


def linhas_max(altura_rect=15, altura_frame=ALTURA_FRAME):
    """Quantas linhas cabem sem estourar o frame."""
    return altura_frame // altura_rect


def get_position(
    indice,
    largura_rect=50,
    altura_rect=15,
    largura_frame=LARGURA_FRAME,
    altura_frame=ALTURA_FRAME,
):
    """
    Retorna (x, y) para o índice dado, quebrando linha automaticamente
    com base no que cabe no frame (largura_frame x altura_frame).
    """
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha

    max_linhas = linhas_max(altura_rect, altura_frame)
    if row >= max_linhas:
        raise ValueError(
            f"Índice {indice} excede a capacidade do frame "
            f"({por_linha} x {max_linhas} = {por_linha * max_linhas} apartamentos). "
            f"TODO: implementar segunda folha quando isso acontecer."
        )

    x = col * largura_rect
    y = -row * altura_rect  # desce a cada linha nova
    return (x, y)


def inverter_indice(indice, total):
    """
    Inverte a ordem: o item que seria o último passa a ser o primeiro
    e vice-versa. As posições do grid continuam as mesmas, só muda
    qual Plaq cai em qual posição.
    (Mantido por compatibilidade — get_position_topo_invertido é o
    método correto para o "linha incompleta no topo".)
    """
    return total - 1 - indice


def get_position_topo_invertido(
    indice,
    total,
    largura_rect=50,
    altura_rect=15,
    largura_frame=LARGURA_FRAME,
    altura_frame=ALTURA_FRAME,
):
    """
    Mesma sequência, mesma leitura esquerda->direita, mas a linha
    incompleta (o resto que sobra) fica no TOPO em vez de ficar
    solta embaixo. As linhas completas ficam abaixo, na ordem normal.
    """
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha

    total_linhas = math.ceil(total / por_linha)
    row_final = total_linhas - 1 - row

    x = col * largura_rect
    y = -row_final * altura_rect
    return (x, y)
