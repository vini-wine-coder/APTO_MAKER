from handmade import fit_text_height  # sua função existente


def draw_plaq(msp, plaq, x, y, largura=50, altura=15):
    # retângulo
    pontos = [
        (x, y),
        (x + largura, y),
        (x + largura, y + altura),
        (x, y + altura),
        (x, y),
    ]
    msp.add_lwpolyline(pontos, close=True)

    # mtext centralizado
    mtext = msp.add_mtext(
        plaq.nome,
        dxfattribs={
            "style": "Arial",
            "char_height": fit_text_height(plaq.nome, largura, altura, base_height=4),
        },
    )
    mtext.set_location(
        insert=(x + largura / 2, y + altura / 2), attachment_point=5
    )  # 5 = middle-center
