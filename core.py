import ezdxf
import constructor
import layout
import drawer

COR = 5  # ACI: 1=vermelho, 2=amarelo, 3=verde, 4=ciano, 5=azul, 6=magenta, 7=branco/preto
LARGURA_BORDA = 660
ALTURA_BORDA = 490
OFFSET_ENTRE_FOLHAS = 10


def gerar_dxf(texto_bruto: str, caminho_saida: str) -> dict:
    """
    Recebe o texto bruto (sequência APTO, uma por linha) e o caminho
    onde salvar o .dxf. Faz todo o pipeline: parse -> paginação em
    folhas -> desenho (3 passes: 50x15, 40x15, 40x15) -> salva.

    Retorna um dict com um resumo do que foi gerado.
    Lança ValueError se o texto não tiver nenhum APTO reconhecível.
    """
    lines = texto_bruto.splitlines()
    obj_sequenc = constructor.plano(lines)

    if not obj_sequenc:
        raise ValueError("Nenhum APTO encontrado no texto fornecido.")

    doc = ezdxf.new(dxfversion="R2010")  # DXF 2010/2011, compatível com ZWCAD
    if "Arial" not in doc.styles:
        doc.styles.new("Arial", dxfattribs={"font": "arial.ttf"})

    msp = doc.modelspace()

    capacidade = layout.capacidade_por_folha(
        altura_borda=ALTURA_BORDA, larguras_passes=(50, 40, 40)
    )
    folhas = layout.particionar_em_folhas(obj_sequenc, capacidade)

    for sheet_idx, folha in enumerate(folhas):
        x_offset = sheet_idx * (LARGURA_BORDA + OFFSET_ENTRE_FOLHAS)
        total_folha = len(folha)

        x0_borda, y0_borda = layout.get_position_topo_invertido(0, total_folha)
        x0_borda += x_offset
        drawer.draw_border(
            msp, largura=LARGURA_BORDA, altura=ALTURA_BORDA,
            x0=x0_borda, y0=y0_borda, cor=1,
        )

        # passe 1: 50x15
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_topo_invertido(local_idx, total_folha)
            drawer.draw_plaq(msp, plaq, x + x_offset, y, cor=COR)

        topo1 = 15  # constante, sempre 0 + altura_rect

        # passe 2: 40x15, começa no topo do passe 1
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_com_offset(
                local_idx, largura_rect=40, altura_rect=10, y_offset=topo1
            )
            drawer.draw_plaq(msp, plaq, x + x_offset, y, largura=40, altura=10, cor=COR)

        topo2 = layout.topo_da_grade(total_folha, largura_rect=40, altura_rect=10, y_offset=topo1)

        # passe 3: 40x15 de novo, começa no topo do passe 2
        for local_idx, plaq in enumerate(folha):
            x, y = layout.get_position_com_offset(
                local_idx, largura_rect=40, altura_rect=10, y_offset=topo2
            )
            drawer.draw_plaq(msp, plaq, x + x_offset, y, largura=40, altura=10, cor=COR)

    doc.saveas(caminho_saida)

    return {
        "total": len(obj_sequenc),
        "folhas": len(folhas),
        "capacidade_por_folha": capacidade,
        "caminho": caminho_saida,
    }
