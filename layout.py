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
