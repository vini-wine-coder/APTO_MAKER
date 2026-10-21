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

# Modos de desenho: cada um e a lista de passadas (largura, altura), nesta ordem.
# Os furos so aparecem nas placas de 50 de largura (regra do drawer).
MODOS = {
    "normal": ((50, 15), (40, 10), (40, 10)),  # 1x 50x15 e 2x 40x10
    "50x15": ((50, 15),),                       # so 50x15
    "40x10": ((40, 10),),                       # so 40x10, uma vez
}
MODO_PADRAO = "normal"


def contar_placas(texto: str) -> int:
    """Quantas placas (linhas nao vazias) o texto tem. Usado pela GUI para mostrar a contagem de cada sequencia."""
    return len(constructor.plano(texto.splitlines()))


def desenhar_sequencia(msp, plaqs, x0, y0, passes):
    """
    Desenha UMA sequencia como uma linha de folhas, lado a lado.
    (x0, y0) e o canto inferior esquerdo da primeira folha.
    `passes` e a lista de (largura, altura) de cada passada (veja MODOS).
    Retorna quantas folhas foram desenhadas.

    Cada sequencia passa por gerar_linhas/distribuir_em_folhas sozinha,
    entao a regra "todas as linhas de uma passada primeiro, depois as da
    proxima" vale por sequencia, sem misturar uma com a outra.
    """
    linhas = layout.gerar_linhas(plaqs, passes)
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
    `sequencias` e uma lista de (nome, texto_bruto, modo), onde `modo` e uma
    chave de MODOS. Gera UM arquivo .dxf com uma linha de folhas por
    sequencia, de cima pra baixo, na ordem da lista.

    Cada linha nao vazia do texto vira uma placa. Sequencias sem nenhuma
    linha sao puladas e devolvidas em "puladas".
    Lanca ValueError se os nomes se repetirem, se algum modo for desconhecido
    ou se todas as sequencias estiverem vazias.
    """
    nomes = [nome for nome, _, _ in sequencias]
    if len(set(nomes)) != len(nomes):
        raise ValueError("Existem sequências com o mesmo nome.")

    for nome, _, modo in sequencias:
        if modo not in MODOS:
            raise ValueError(f'Modo de desenho desconhecido em "{nome}": {modo!r}.')

    doc = ezdxf.new(dxfversion="R2010")
    if "Arial" not in doc.styles:
        doc.styles.new("Arial", dxfattribs={"font": "arial.ttf"})
    msp = doc.modelspace()

    y0 = 0
    total_placas = 0
    total_folhas = 0
    desenhadas = 0
    puladas = []

    for nome, texto, modo in sequencias:
        plaqs = constructor.plano(texto.splitlines())

        if not plaqs:
            puladas.append(nome)
            continue

        total_folhas += desenhar_sequencia(msp, plaqs, X0, y0, MODOS[modo])
        drawer.draw_nome_sequencia(msp, nome, X0 - OFFSET_NOME, y0, altura_texto=ALTURA_NOME)
        total_placas += len(plaqs)
        desenhadas += 1
        y0 -= ALTURA_BORDA + GAP_ENTRE_LINHAS  # proxima sequencia vai uma linha abaixo

    if desenhadas == 0:
        raise ValueError("Não há nada para desenhar: todas as sequências estão vazias.")

    doc.saveas(caminho_saida)

    return {
        "sequencias": desenhadas,
        "total": total_placas,
        "folhas": total_folhas,
        "puladas": puladas,
        "caminho": caminho_saida,
    }
