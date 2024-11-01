from enum import IntEnum, StrEnum


# Gestos que podm ser reconhecidos
class Escolha(StrEnum):
    PEDRA = "pedra"
    PAPEL = "papel"
    TESOURA = "tesoura"


# Resultado das rodadas e partida
class Resultado(IntEnum):
    EMPATE = 0
    JOGADOR1 = 1
    JOGADOR2 = 2


# Enumera os jogadores
class Jogadores(IntEnum):
    JOGADOR1 = 1
    JOGADOR2 = 2
