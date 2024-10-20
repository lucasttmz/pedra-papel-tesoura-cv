from enum import IntEnum, StrEnum


class Escolha(StrEnum):
    PEDRA = "pedra"
    PAPEL = "papel"
    TESOURA = "tesoura"


class Resultado(IntEnum):
    EMPATE = 0
    JOGADOR1 = 1
    JOGADOR2 = 2
