import ezdxf
import constructor
import layout
import drawer

COR = 5  # ACI: 1=vermelho, 2=amarelo, 3=verde, 4=ciano, 5=azul, 6=magenta, 7=branco/preto
LARGURA_BORDA = 660
ALTURA_BORDA = 490
ALTURA_DISPONIVEL = 360  # orcamento real de conteudo por folha (deixa margem dentro da borda)
OFFSET_ENTRE_FOLHAS = 10
GAP_ENTRE_LINHAS = 10  # espaco vertical entre a linha de uma sequencia e a proxima
X0 = 0  # onde cada sequencia comeca em x (todas alinhadas na mesma coluna)
OFFSET_NOME = 30  # o nome da sequencia e escrito em (X0 - OFFSET_NOME, y0)
ALTURA_NOME = 10  # altura do texto do nome
PASSES = ((50, 15), (40, 10), (40, 10)) # (largura, altura) de cada passada, nesta ordem

def contar_aptos(texto: str) -> int:
    """Quantos APTOs o texto tem. Usado pela GUI para mostrar a contagem de cada sequencia."""
    return len(constructor.plano(texto.splitlines()))



def desenhar_sequencia(msp, plaqs, x0, y0):
    """
    Desenha UMA sequencia como uma linha de folhas, lado a lado.
    (x0, y0) e o canto inferior esquerdo da primeira folha.
    Retorna quantas folhas foram desenhadas.
    """
    linhas = layout.gerar_linhas(plaqs, PASSES)
    folhas = layout.distribuir_em_folhas(linhas, altura_disponivel=ALTURA_DISPONIVEL)

    for sheet_idx, folha in enumerate(folhas):
        x_folha = x0 + sheet_idx * (LARGURA_BORDA + OFFSET_ENTRE_FOLHAS)

        drawer.draw_border(
            msp, largura=LARGURA_BORDA, altura=ALTURA_BORDA,
            x0=x_folha, y0=y0, cor=1,
        )

        for linha, y_local in folha:
            largura_rect = linha["largura"]
            altura_rect = linha["altura"]
            for col_idx, plaq in enumerate(linha["itens"]):
                x = x_folha + col_idx * largura_rect
                y = y0 + y_local
                drawer.draw_plaq(msp, plaq, x, y, largura=largura_rect, altura=altura_rect, cor=COR)

    return len(folhas)


def gerar_dxf(sequencias, caminho_saida: str) -> dict:
    """
    `sequencias` e uma lista de (nome, texto_bruto). Gera UM arquivo .dxf
    com uma linha de folhas por sequencia, de cima pra baixo, na ordem da lista.
    """
    nomes = [nome for nome, _ in sequencias]
    if len(set(nomes)) != len(nomes):
        raise ValueError("Existem sequências com o mesmo nome.")

    doc = ezdxf.new(dxfversion="R2010")
    if "Arial" not in doc.styles:
        doc.styles.new("Arial", dxfattribs={"font": "arial.ttf"})
    msp = doc.modelspace()

    y0 = 0
    total_aptos = 0
    total_folhas = 0
    desenhadas = 0
    puladas = []

    for nome, texto in sequencias:
        plaqs = constructor.plano(texto.splitlines())

        if not plaqs:
            puladas.append(nome)
            continue

        total_folhas += desenhar_sequencia(msp, plaqs, X0, y0)
        drawer.draw_nome_sequencia(msp, nome, X0 - OFFSET_NOME, y0, altura_texto=ALTURA_NOME)
        total_aptos += len(plaqs)
        desenhadas += 1
        y0 -= ALTURA_BORDA + GAP_ENTRE_LINHAS  # proxima sequencia vai uma linha abaixo

    if desenhadas == 0:
        raise ValueError("Nenhum APTO encontrado nas sequências fornecidas.")

    doc.saveas(caminho_saida)

    return {
        "sequencias": desenhadas,
        "total": total_aptos,
        "folhas": total_folhas,
        "puladas": puladas,
        "caminho": caminho_saida,
    }
