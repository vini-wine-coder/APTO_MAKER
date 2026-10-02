import math

LARGURA_FRAME = 620
ALTURA_FRAME = 550


def por_linha_max(largura_rect=50, largura_frame=LARGURA_FRAME):
    return largura_frame // largura_rect


def get_position(indice, largura_rect=50, altura_rect=15, largura_frame=LARGURA_FRAME):
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha
    x = col * largura_rect
    y = row * altura_rect
    return (x, y)


def get_position_topo_invertido(indice, total, largura_rect=50, altura_rect=15,
                                 largura_frame=LARGURA_FRAME):
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha
    total_linhas = math.ceil(total / por_linha)
    row_final = total_linhas - 1 - row
    x = col * largura_rect
    y = -row_final * altura_rect
    return (x, y)


def get_position_com_offset(indice, largura_rect=50, altura_rect=15,
                             largura_frame=LARGURA_FRAME, y_offset=0):
    por_linha = por_linha_max(largura_rect, largura_frame)
    col = indice % por_linha
    row = indice // por_linha
    x = col * largura_rect
    y = y_offset + row * altura_rect
    return (x, y)


def topo_da_grade(total, largura_rect=50, altura_rect=15,
                   largura_frame=LARGURA_FRAME, y_offset=0):
    por_linha = por_linha_max(largura_rect, largura_frame)
    total_linhas = math.ceil(total / por_linha)
    return y_offset + total_linhas * altura_rect


def capacidade_por_folha(altura_borda=490, altura_rect=15,
                          largura_frame=LARGURA_FRAME,
                          larguras_passes=(50, 40, 40)):
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
    return [obj_sequenc[i:i + capacidade] for i in range(0, len(obj_sequenc), capacidade)]
