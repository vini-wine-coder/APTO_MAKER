import ezdxf
import constructor
import layout
import drawer


LARGURA_BORDA = 660
ALTURA_BORDA = 490
OFFSET_ENTRE_FOLHAS = 10


def read_multiline_input():
    print("Digite a sequência APTO (linha vazia para finalizar):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return lines


lines = read_multiline_input()
obj_sequenc = constructor.plano(lines)

doc = ezdxf.new()
msp = doc.modelspace()

total = len(obj_sequenc)


def draw_border(msp, largura, altura, x0, y0):
    cor = 1
    altura = altura * -1
    pontos = [
        (x0, y0),
        (x0 + largura, y0),
        (x0 + largura, y0 - altura),
        (x0, y0 - altura),
        (x0, y0),
    ]
    msp.add_lwpolyline(pontos, close=True, dxfattribs={"color": cor})


def draw_dxf_50x15():
    capacidade = layout.capacidade_por_folha(
        altura_borda=ALTURA_BORDA, larguras_passes=(50, 40, 40)
    )
    folhas = layout.particionar_em_folhas(obj_sequenc, capacidade)

    for sheet_idx, folha in enumerate(folhas):
        x_offset = sheet_idx * (LARGURA_BORDA + OFFSET_ENTRE_FOLHAS)
        total_folha = len(folha)

        x0_borda, y0_borda = layout.get_position_topo_invertido(0, total_folha)
        x0_borda += x_offset
        draw_border(
            msp,
            largura=LARGURA_BORDA,
            altura=ALTURA_BORDA,
            x0=x0_borda,
            y0=y0_borda,
        )

        # passe 1: 50x15
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_topo_invertido(local_idx, total_folha)
            drawer.draw_plaq(msp, plaq, x + x_offset, y)

        topo1 = 15  # constante, sempre 0 + altura_rect

        # passe 2: 40x15, começa no topo do passe 1
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_com_offset(
                local_idx, largura_rect=40, altura_rect=15, y_offset=topo1
            )
            drawer.draw_plaq(msp, plaq, x + x_offset, y, largura=40, altura=15)

        topo2 = layout.topo_da_grade(
            total_folha, largura_rect=40, altura_rect=15, y_offset=topo1
        )

        # passe 3: 40x15 de novo, começa no topo do passe 2
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_com_offset(
                local_idx, largura_rect=40, altura_rect=15, y_offset=topo2
            )
            drawer.draw_plaq(msp, plaq, x + x_offset, y, largura=40, altura=15)


draw_dxf_50x15()

doc.saveas("./dxf_files/output.dxf")
print(f"{total} apartamentos desenhados em output.dxf")
