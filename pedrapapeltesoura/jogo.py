from abc import ABC, abstractmethod

from constantes import Escolha, Resultado
from visualizacao import Janela


class Jogo:
    CONTAGEM_MAXIMA = 3
    RODADAS = 1

    def __init__(self, janela: Janela) -> None:
        self.estado_atual: Estado = EstadoNaoIniciado()
        self.view = janela
        self.resultado: Resultado = Resultado.EMPATE
        self.movimento_jogador1: Escolha | None = None
        self.movimento_jogador2: Escolha | None = None
        self.pontuacao_jogador1 = 0
        self.pontuacao_jogador2 = 0
        self.rodada_atual = 1
        self.tempo_restante = Jogo.CONTAGEM_MAXIMA
        self.encerrado = False

    def atualizar_jogo(self, frame):
        self.estado_atual.proximo_estado(self, frame)


class Estado(ABC):
    @abstractmethod
    def proximo_estado(self, jogo: Jogo, frame):
        pass


class EstadoNaoIniciado(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        jogo.estado_atual = EstadoContagemRegressiva()


class EstadoContagemRegressiva(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        if jogo.tempo_restante > 0:
            jogo.view.atualizar_contador(jogo.tempo_restante, frame)
            jogo.tempo_restante -= 1
        else:
            jogo.estado_atual = EstadoProcessandoMovimento()


class EstadoProcessandoMovimento(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        jogo.movimento_jogador1, jogo.movimento_jogador2 = jogo.view.ler_movimento(frame)
        jogo.estado_atual = EstadoExibindoMovimentos()


class EstadoExibindoMovimentos(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        jogo.view.mostrar_movimentos(jogo.movimento_jogador1, jogo.movimento_jogador2, frame)
        jogo.estado_atual = EstadoVerificandoVencedor()


class EstadoVerificandoVencedor(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        # Determina quem venceu
        escolhas = list(Escolha)
        indice_jogador1 = escolhas.index(jogo.movimento_jogador1) #type: ignore
        indice_jogador2 = escolhas.index(jogo.movimento_jogador2) #type: ignore
        resultado = (indice_jogador1 - indice_jogador2) % 3

        # Aumenta a pontuação
        jogo.resultado = Resultado(resultado)
        if jogo.resultado == Resultado.JOGADOR1:
            jogo.pontuacao_jogador1 += 1
        elif jogo.resultado == Resultado.JOGADOR2:
            jogo.pontuacao_jogador2 += 1

        jogo.estado_atual = EstadoExibindoResultado()


class EstadoExibindoResultado(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        movimentos = [None, jogo.movimento_jogador1, jogo.movimento_jogador2]
        movimento_vencedor = movimentos[jogo.resultado] 
        jogo.view.mostrar_resultado(jogo.resultado, movimento_vencedor, frame)
        jogo.estado_atual = EstadoAguardandoProximaRodada()


class EstadoAguardandoProximaRodada(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        jogo.rodada_atual += 1
        if jogo.rodada_atual <= Jogo.RODADAS:
            jogo.tempo_restante = Jogo.CONTAGEM_MAXIMA
            jogo.estado_atual = EstadoContagemRegressiva()
        else:
            if jogo.pontuacao_jogador1 == jogo.pontuacao_jogador2:
                jogo.resultado = Resultado.EMPATE
            elif jogo.pontuacao_jogador1 > jogo.pontuacao_jogador2:
                jogo.resultado = Resultado.JOGADOR1
            else:
                jogo.resultado = Resultado.JOGADOR2
    
            jogo.estado_atual = EstadoEncerrado()


class EstadoEncerrado(Estado):
    def proximo_estado(self, jogo: Jogo, frame):
        jogo.encerrado = True
        jogo.view.mostrar_resultado_final(jogo.resultado, jogo.pontuacao_jogador1, jogo.pontuacao_jogador2, frame)
