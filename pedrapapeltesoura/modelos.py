from enum import IntEnum, StrEnum


class Estado(IntEnum):
    NAO_INICIADO = 0
    CONTAGEM_REGRESSIVA = 1
    PROCESSANDO_MOVIMENTO = 2
    EXIBINDO_MOVIMENTOS = 3
    VERIFICANDO_VENCEDOR = 4
    EXIBINDO_RESULTADO = 5
    AGUARDANDO_PROXIMA_RODADA = 6
    ENCERRADO = 7


class Escolha(StrEnum):
    PEDRA = "pedra"
    PAPEL = "papel"
    TESOURA = "tesoura"


class Resultado(IntEnum):
    EMPATE = 0
    JOGADOR1 = 1
    JOGADOR2 = 2
