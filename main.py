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

for plaq in obj_sequenc:
    x, y = layout.get_position(plaq.indice)
    drawer.draw_plaq(msp, plaq, x, y)

doc.saveas("output.dxf")
