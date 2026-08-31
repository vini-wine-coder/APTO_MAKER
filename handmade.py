FONT_WIDTH_FACTOR = (
    0.6  # aproximação largura/altura para Arial; ajuste se o texto ainda estourar
)


def fit_text_height(texto, largura_caixa, altura_caixa, base_height=4, margem=0.9):
    """
    Calcula a altura de char_height do MTEXT que melhor cabe dentro da caixa,
    sem estourar nem a largura nem a altura disponível.

    - base_height: altura desejada por padrão (ex: 4)
    - margem: fração da caixa que o texto pode ocupar (0.9 = 90%, deixa uma folga)
    """
    largura_disponivel = largura_caixa * margem
    altura_disponivel = altura_caixa * margem

    # estima a largura que o texto teria na altura base
    largura_estimada = len(texto) * base_height * FONT_WIDTH_FACTOR

    altura = base_height

    # se o texto for largo demais pra caixa, reduz a altura proporcionalmente
    if largura_estimada > largura_disponivel:
        altura = largura_disponivel / (len(texto) * FONT_WIDTH_FACTOR)

    # nunca deixa a altura passar do que cabe verticalmente na caixa
    altura = min(altura, altura_disponivel)

    return altura
