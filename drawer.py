from handmade import fit_text_height  # sua função existente

COR_PADRAO = 7  # branco/preto (ACI - AutoCAD Color Index)


def draw_plaq(msp, plaq, x, y, largura=50, altura=15, cor=COR_PADRAO):
    # os furos só existem na passada de 50 largura (pass 1).
    # 40x10 (passes 2 e 3) não tem furo.
    desenha_furos = largura >= 50

    # retângulo
    pontos = [
        (x, y),
        (x + largura, y),
        (x + largura, y + altura),
        (x, y + altura),
        (x, y),
    ]
    msp.add_lwpolyline(pontos, close=True, dxfattribs={"color": cor})

    # mtext centralizado
    mtext = msp.add_mtext(
        plaq.nome,
        dxfattribs={
            "style": "Arial",
            "char_height": fit_text_height(plaq.nome, largura, altura, base_height=4),
            "color": 0,
        },
    )
    mtext.set_location(
        insert=(x + largura / 2, y + altura / 2), attachment_point=5
    )  # 5 = middle-center

    if desenha_furos:
        x_circle = x + 4
        y_circle = y + altura / 2  # centro vertical (equivale a +7.5 quando altura=15)
        x_scaling = x_circle + 42
        msp.add_circle((x_circle, y_circle), radius=1.5, dxfattribs={"color": 1})
        msp.add_circle((x_scaling, y_circle), radius=1.5, dxfattribs={"color": 1})


def draw_border(msp, largura, altura, x0, y0, cor=1):
    pontos = [
        (x0, y0),
        (x0 + largura, y0),
        (x0 + largura, y0 + altura),
        (x0, y0 + altura),
        (x0, y0),
    ]
    msp.add_lwpolyline(pontos, close=True, dxfattribs={"color": cor})
