import ezdxf
import constructor
import layout
import drawer

COR = 5  # ACI: 1=vermelho, 2=amarelo, 3=verde, 4=ciano, 5=azul, 6=magenta, 7=branco/preto
LARGURA_BORDA = 660
ALTURA_BORDA = 490
ALTURA_DISPONIVEL = 360  # orçamento real de conteúdo por folha (deixa margem dentro da borda)
OFFSET_ENTRE_FOLHAS = 10
PASSES = ((50, 15), (40, 10), (40, 10))  # (largura, altura) de cada passada, nesta ordem


def gerar_dxf(texto_bruto: str, caminho_saida: str) -> dict:
    """
    Pipeline completo: parse -> gera linhas (todas as 50x15 primeiro,
    depois todas as 40x10, depois todas as 40x10 de novo) -> distribui
    essas linhas em folhas (fluxo contínuo, sem reiniciar por passada)
    -> desenha -> salva.
    """
    lines = texto_bruto.splitlines()
    obj_sequenc = constructor.plano(lines)

    if not obj_sequenc:
        raise ValueError("Nenhum APTO encontrado no texto fornecido.")

    doc = ezdxf.new(dxfversion="R2010")
    if "Arial" not in doc.styles:
        doc.styles.new("Arial", dxfattribs={"font": "arial.ttf"})

    msp = doc.modelspace()

    linhas = layout.gerar_linhas(obj_sequenc, PASSES)
    folhas = layout.distribuir_em_folhas(linhas, altura_disponivel=ALTURA_DISPONIVEL)

    for sheet_idx, folha in enumerate(folhas):
        x_offset = sheet_idx * (LARGURA_BORDA + OFFSET_ENTRE_FOLHAS)

        # borda desta folha: ancorada no topo (y0=ALTURA_BORDA), estende
        # pra baixo até y=0 — onde o conteúdo (y positivo, de baixo pra
        # cima) começa.
        drawer.draw_border(
            msp, largura=LARGURA_BORDA, altura=ALTURA_BORDA,
            x0=x_offset, y0=0, cor=1,
        )

        for linha, y_local in folha:
            largura_rect = linha["largura"]
            altura_rect = linha["altura"]
            for col_idx, plaq in enumerate(linha["itens"]):
                x = col_idx * largura_rect + x_offset
                y = y_local
                drawer.draw_plaq(msp, plaq, x, y, largura=largura_rect, altura=altura_rect, cor=COR)

    doc.saveas(caminho_saida)

    return {
        "total": len(obj_sequenc),
        "folhas": len(folhas),
        "caminho": caminho_saida,
    }
