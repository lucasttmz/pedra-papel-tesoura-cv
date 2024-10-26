from abc import ABC, abstractmethod

from constantes import Escolha, Resultado
from visualizacao import Janela


class Jogo:
    CONTAGEM_MAXIMA = 3
    TOTAL_RODADAS = 1

    def __init__(self, janela: Janela, rodadas: int = TOTAL_RODADAS) -> None:
        self.estado_atual: Estado = EstadoNaoIniciado()
        self.view = janela
        self.resultado: Resultado = Resultado.EMPATE
        self.movimento_jogador1: Escolha | None = None
        self.movimento_jogador2: Escolha | None = None
        self.pontuacao_jogador1 = 0
        self.pontuacao_jogador2 = 0
        self.rodadas = rodadas
        self.rodada_atual = 1
        self.tempo_restante = Jogo.CONTAGEM_MAXIMA
        self.encerrado = False

    def atualizar_jogo(self, frame):
        self.estado_atual.atualizar(self, frame)

    def alterar_estado(self, proximo_estado):
        self.estado_atual = proximo_estado


class Estado(ABC):
    @abstractmethod
    def atualizar(self, jogo: Jogo, frame):
        pass


class EstadoNaoIniciado(Estado):
    """ 
    Transições:
        Não Iniciado -> Contagem Regressiva
    """
    def atualizar(self, jogo: Jogo, frame):
        jogo.alterar_estado(EstadoContagemRegressiva())


class EstadoContagemRegressiva(Estado):
    """ 
    Transições:
        Contagem Regressiva -> Contagem Regressiva
        Contagem Regressiva -> Processando Movimento
    """
    def atualizar(self, jogo: Jogo, frame):
        if jogo.tempo_restante > 0:
            jogo.view.atualizar_contador(jogo.tempo_restante, frame)
            jogo.tempo_restante -= 1
        else:
            jogo.alterar_estado(EstadoProcessandoMovimento())


class EstadoProcessandoMovimento(Estado):
    """ 
    Transições:
        Processando Movimento -> Exibindo Movimentos
    """
    def atualizar(self, jogo: Jogo, frame):
        jogo.movimento_jogador1, jogo.movimento_jogador2 = jogo.view.ler_movimento(frame)
        jogo.alterar_estado(EstadoExibindoMovimentos())


class EstadoExibindoMovimentos(Estado):
    """ 
    Transições:
        Exibindo Movimentos -> Verificando Vencedor
    """
    def atualizar(self, jogo: Jogo, frame):
        jogo.view.mostrar_movimentos(jogo.movimento_jogador1, jogo.movimento_jogador2, frame)
        jogo.alterar_estado(EstadoVerificandoVencedor())


class EstadoVerificandoVencedor(Estado):
    """ 
    Transições:
        Verificando Vencedor -> Exibindo Resultado
    """
    def atualizar(self, jogo: Jogo, frame):
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

        jogo.alterar_estado(EstadoExibindoResultado())


class EstadoExibindoResultado(Estado):
    """ 
    Transições:
        Exibindo Resultado -> Aguardando Próxima Rodada
    """
    def atualizar(self, jogo: Jogo, frame):
        movimentos = [None, jogo.movimento_jogador1, jogo.movimento_jogador2]
        movimento_vencedor = movimentos[jogo.resultado] 
        jogo.view.mostrar_resultado(jogo.resultado, movimento_vencedor, frame)
        jogo.alterar_estado(EstadoAguardandoProximaRodada())


class EstadoAguardandoProximaRodada(Estado):
    """ 
    Transições:
        Aguardando Próxima Rodada -> Contagem Regressiva
        Aguardando Próxima Rodada -> Encerrado
    """
    def atualizar(self, jogo: Jogo, frame):
        jogo.rodada_atual += 1
        if jogo.rodada_atual <= jogo.rodadas:
            jogo.tempo_restante = Jogo.CONTAGEM_MAXIMA
            jogo.alterar_estado(EstadoContagemRegressiva())
        else:
            if jogo.pontuacao_jogador1 == jogo.pontuacao_jogador2:
                jogo.resultado = Resultado.EMPATE
            elif jogo.pontuacao_jogador1 > jogo.pontuacao_jogador2:
                jogo.resultado = Resultado.JOGADOR1
            else:
                jogo.resultado = Resultado.JOGADOR2
    
            jogo.alterar_estado(EstadoEncerrado())


class EstadoEncerrado(Estado):
    """ 
    Transições:
        ---
    """
    def atualizar(self, jogo: Jogo, frame):
        jogo.encerrado = True
        jogo.view.mostrar_resultado_final(jogo.resultado, jogo.pontuacao_jogador1, jogo.pontuacao_jogador2, frame)
