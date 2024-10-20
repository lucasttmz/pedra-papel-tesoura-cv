from modelos import Escolha, Estado, Resultado
from visualizacao import Render

class Jogo:
    CONTAGEM_MAXIMA = 3
    RODADAS = 3

    def __init__(self, view: Render) -> None:
        self.view = view
        self.estado: Estado = Estado.NAO_INICIADO
        self.resultado: Resultado | None = None
        self.movimento_jogador1: Escolha | None = None
        self.movimento_jogador2: Escolha | None = None
        self.pontuacao_jogador1 = 0
        self.pontuacao_jogador2 = 0
        self.rodada_atual = 1

    def iniciar_jogo(self) -> None:
        if self.estado != Estado.NAO_INICIADO:
            raise ValueError(f"Impossível iniciar o jogo no estado atual {self.estado}")
        
        self.tempo_restante = Jogo.CONTAGEM_MAXIMA
        self.estado = Estado.CONTAGEM_REGRESSIVA

    def atualizar_contagem_regressiva(self) -> None:
        if self.estado != Estado.CONTAGEM_REGRESSIVA:
            raise ValueError(f"Impossível atualizar contagem no estado atual {self.estado}")
        
        if self.tempo_restante > 0:
            self.view.atualizar_contador(self.tempo_restante)
            self.tempo_restante -= 1
        else:
            self.estado = Estado.PROCESSANDO_MOVIMENTO

    def processar_movimentos(self) -> None:
        if self.estado != Estado.PROCESSANDO_MOVIMENTO:
            raise ValueError(f"Impossível processar movimentos no estado atual {self.estado}")

        self.movimento_jogador1, self.movimento_jogador2 = self.view.ler_movimento()
        self.estado = Estado.EXIBINDO_MOVIMENTOS

    def verificar_vencedor(self) -> None:
        if self.estado != Estado.VERIFICANDO_VENCEDOR:
            raise ValueError(f"Impossível verificar vencedor no estado atual {self.estado}")
        
        escolhas = list(Escolha)
        indice_jogador1 = escolhas.index(self.movimento_jogador1) #type: ignore
        indice_jogador2 = escolhas.index(self.movimento_jogador2) #type: ignore
        resultado = (indice_jogador1 - indice_jogador2) % 3

        self.resultado = Resultado(resultado)
        if self.resultado == Resultado.JOGADOR1:
            self.pontuacao_jogador1 += 1
        elif self.resultado == Resultado.JOGADOR2:
            self.pontuacao_jogador2 += 1
        
        self.estado = Estado.EXIBINDO_RESULTADO

    def exibir_movimentos_detectados(self):
        if self.estado != Estado.EXIBINDO_MOVIMENTOS:
            raise ValueError(f"Impossível exibir movimentos no estado atual {self.estado}")
        
        self.view.mostrar_movimentos(self.movimento_jogador1, self.movimento_jogador2)
        self.estado = Estado.VERIFICANDO_VENCEDOR

    def exibir_resultado_rodada(self):
        if self.estado != Estado.EXIBINDO_RESULTADO or self.resultado is None:
            raise ValueError(f"Impossível exibir resultado no estado atual {self.estado}")
    
        movimentos = [None, self.movimento_jogador1, self.movimento_jogador2]
        movimento_vencedor = movimentos[self.resultado]
        self.view.mostrar_resultado(self.resultado, movimento_vencedor)
        self.estado = Estado.AGUARDANDO_PROXIMA_RODADA

    def proxima_rodada(self):
        if self.estado != Estado.AGUARDANDO_PROXIMA_RODADA:
            raise ValueError(f"Impossível exibir resultado da rodada no estado atual {self.estado}")
        
        self.rodada_atual += 1
        if self.rodada_atual <= Jogo.RODADAS:
            self.estado = Estado.CONTAGEM_REGRESSIVA
        else:
            if self.pontuacao_jogador1 == self.pontuacao_jogador2:
                self.resultado = Resultado.EMPATE
            elif self.pontuacao_jogador1 > self.pontuacao_jogador2:
                self.resultado = Resultado.JOGADOR1
            else:
                self.resultado = Resultado.JOGADOR2
    
            self.estado = Estado.ENCERRADO

    def exibir_resultado_final(self):
        if self.estado != Estado.ENCERRADO or self.resultado is None:
            raise ValueError(f"Impossível exibir resultado final no estado atual {self.estado}")
        
        self.view.mostrar_resultado_final(self.resultado, self.pontuacao_jogador1, self.pontuacao_jogador2)
