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


def get_position_com_offset(
    indice, largura_rect=50, altura_rect=15, largura_frame=LARGURA_FRAME, y_offset=0
):
    """
    Igual a get_position, mas soma um y_offset fixo — útil para
    desenhar uma segunda leva de retângulos começando exatamente
    onde a primeira leva terminou (em cima dela).
    """
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha

    x = col * largura_rect
    y = y_offset + row * altura_rect
    return (x, y)


def topo_da_grade(
    total, largura_rect=50, altura_rect=15, largura_frame=LARGURA_FRAME, y_offset=0
):
    """
    Retorna o y do topo de uma grade desenhada com get_position_com_offset
    (ou seja: y_offset + altura total ocupada pelas linhas). Use esse
    valor como y_offset da próxima leva, para empilhar uma em cima da outra.
    """
    import math

    por_linha = por_linha_max(largura_rect, largura_frame)
    total_linhas = math.ceil(total / por_linha)
    return y_offset + total_linhas * altura_rect


def capacidade_por_folha(
    altura_borda=490,
    altura_rect=15,
    largura_frame=LARGURA_FRAME,
    larguras_passes=(50, 40, 40),
):
    """Calcula quantos apartamentos cabem em uma folha, considerando as 3 passadas."""
    import math

    def altura_total(k):
        total_linhas = 0
        for largura_rect in larguras_passes:
            por_linha = largura_frame // largura_rect
            total_linhas += math.ceil(k / por_linha) if k > 0 else 0
        return total_linhas * altura_rect

    capacidade = 0
    k = 1
    while altura_total(k) <= altura_borda:
        capacidade = k
        k += 1
    return capacidade


def particionar_em_folhas(obj_sequenc, capacidade):
    """Divide a lista em pedaços de no máximo `capacidade` itens."""
    return [
        obj_sequenc[i : i + capacidade] for i in range(0, len(obj_sequenc), capacidade)
    ]
