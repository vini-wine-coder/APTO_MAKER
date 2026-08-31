import re
from Plaq import Plaq

PATTERN = re.compile(r"APTO\s+\S+", re.IGNORECASE)


def plano(lines):
    """
    Recebe uma lista de linhas (strings) já capturadas pelo input,
    extrai cada "APTO XXX" e retorna a lista de objetos Plaq.
    """
    raw_text = " ".join(lines)
    matches = PATTERN.findall(raw_text)
    return [Plaq(match, idx) for idx, match in enumerate(matches)]
