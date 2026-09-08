import ezdxf
import constructor
import layout
import drawer


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


def draw_border(msp, x0, y0):
    cor = 1
    largura = 660
    altura = -490
    pontos = [
        (x0, y0),
        (x0 + largura, y0),
        (x0 + largura, y0 - altura),
        (x0, y0 - altura),
        (x0, y0),
    ]
    msp.add_lwpolyline(pontos, close=True, dxfattribs={"color": cor})


def draw_dxf_50x15():
    for plaq in obj_sequenc:
        x, y = layout.get_position_topo_invertido(plaq.indice, total)
        drawer.draw_plaq(msp, plaq, x, y)
        if plaq.indice == 0:
            draw_border(msp, x, y)  # pega a ultima plaq draw_dxf_50x15
    # topo da primeira grade (50x15) e sempre y=0+15=15, constante
    # topo da 1a grade (50x15, via get_position_topo_invertido) é sempre y=0+15=15
    TOPO_GRADE_1 = 15

    # 2a leva: 40x15, comeca no topo da 1a
    for plaq in obj_sequenc:
        x, y = layout.get_position_com_offset(
            plaq.indice, largura_rect=40, altura_rect=15, y_offset=TOPO_GRADE_1
        )
        drawer.draw_plaq(msp, plaq, x, y, largura=40, altura=15)

    # topo da 2a grade — nao e constante, calculado com base no total
    TOPO_GRADE_2 = layout.topo_da_grade(
        total, largura_rect=40, altura_rect=15, y_offset=TOPO_GRADE_1
    )

    # 3a leva: 40x15 de novo, comeca no topo da 2a
    for plaq in obj_sequenc:
        x, y = layout.get_position_com_offset(
            plaq.indice, largura_rect=40, altura_rect=15, y_offset=TOPO_GRADE_2
        )
        drawer.draw_plaq(msp, plaq, x, y, largura=40, altura=15)


draw_dxf_50x15()

doc.saveas("./dxf_files/output.dxf")
print(f"{total} apartamentos desenhados em output.dxf")
