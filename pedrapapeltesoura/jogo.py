import time

from enum import IntEnum, StrEnum


class Estado(IntEnum):
    NAO_INICIADO = 0
    CONTAGEM_REGRESSIVA = 1
    PROCESSANDO_MOVIMENTO = 2
    EXIBINDO_MOVIMENTOS = 3
    EXIBINDO_RESULTADO = 4
    AGUARDANDO_PROXIMA_RODADA = 5
    ENCERRADO = 6


class Escolha(StrEnum):
    PEDRA = "Pedra"
    PAPEL = "Papel"
    TESOURA = "Tesoura"


class Resultado(IntEnum):
    EMPATE = 0
    JOGADOR1 = 1
    JOGADOR2 = 2


class Jogo:
    CONTAGEM_MAXIMA = 3
    RODADAS = 3

    def __init__(self) -> None:
        self.estado: Estado = Estado.NAO_INICIADO
        self.resultado: Resultado | None = None
        self.movimento_jogador1: Escolha | None = None
        self.movimento_jogador2: Escolha | None = None
        self.pontuacao_jogador1 = 0
        self.pontuacao_jogador2 = 0
        self.rodada_atual = 1

    def iniciar_jogo(self) -> None:
        if self.estado != Estado.NAO_INICIADO:
            raise ValueError("Impossível iniciar o jogo no estado atual")
        
        self.iniciar_contagem_regressiva()

    def iniciar_contagem_regressiva(self) -> None:
        if self.estado not in (Estado.NAO_INICIADO, Estado.EXIBINDO_RESULTADO):
            raise ValueError("Impossível iniciar contagem no estado atual")
        
        self.estado = Estado.CONTAGEM_REGRESSIVA
        self.tempo_restante = Jogo.CONTAGEM_MAXIMA

    def atualizar_contagem_regressiva(self) -> None:
        if self.estado != Estado.CONTAGEM_REGRESSIVA:
            raise ValueError("Impossível atualizar contagem no estado atual")
        
        if self.tempo_restante > 0:
            time.sleep(1)
            self.tempo_restante -= 1
            print(f"{self.tempo_restante}...")
        else:
            print("Já!")
            self.estado = Estado.PROCESSANDO_MOVIMENTO

    def processar_movimentos(self) -> None:
        if self.estado != Estado.PROCESSANDO_MOVIMENTO:
            raise ValueError("Impossível processar movimentos no estado atual")

        while True:
            entrada = input("Jogador 1, escolha: pedra, papel ou tesoura: ")
            try:
                self.movimento_jogador1 = Escolha(entrada.lower())
                break
            except ValueError:
                print("Escolha inválida! Escolha entre: pedra, papel ou tesoura.")

        while True:
            entrada = input("Jogador 2, escolha: pedra, papel ou tesoura: ")
            try:
                self.movimento_jogador2 = Escolha(entrada.lower())
                break
            except ValueError:
                print("Escolha inválida! Escolha entre: pedra, papel ou tesoura.")
        
        print(f"{self.movimento_jogador1} x {self.movimento_jogador2}")
        self.verificar_vencedor((self.movimento_jogador1, self.movimento_jogador2))
        self.estado = Estado.EXIBINDO_MOVIMENTOS

    def exibir_movimentos(self):
        if self.estado != Estado.PROCESSANDO_MOVIMENTO:
            raise ValueError("Impossível verificar vencedor no estado atual")
        
        self.estado = Estado.EXIBINDO_RESULTADO

    def verificar_vencedor(self, movimentos: tuple[Escolha, Escolha]) -> None:
        if self.estado != Estado.PROCESSANDO_MOVIMENTO:
            raise ValueError("Impossível verificar vencedor no estado atual")
        
        jogador1, jogador2 = movimentos
        escolhas = [Escolha.PEDRA, Escolha.PAPEL, Escolha.TESOURA]
        indice_jogador1 = escolhas.index(jogador1)
        indice_jogador2 = escolhas.index(jogador2)
        resultado = (indice_jogador1 - indice_jogador2) % 3
        self.resultado = Resultado(resultado)
        self.atualizar_pontuacao()

    def atualizar_pontuacao(self):
        if self.resultado != Estado.PROCESSANDO_MOVIMENTO:
            raise ValueError("Impossível atualizar pontuação no estado atual")
        
        if self.resultado == Resultado.JOGADOR1:
            self.pontuacao_jogador1 += 1
        elif self.resultado == Resultado.JOGADOR2:
            self.pontuacao_jogador2 += 1
        else:
            return # Empate

    def exibir_resultado_rodada(self):
        if self.estado != Estado.EXIBINDO_RESULTADO or self.resultado is None:
            raise ValueError("Impossível exibir resultado no estado atual")
    
        movimentos = [self.movimento_jogador1, self.movimento_jogador2, None]
        movimento_vencedor = movimentos[self.resultado]
        if self.resultado == Resultado.EMPATE:
            print(f"Empate!")
        else:
            print(f"Jogador {self.resultado} venceu utilizando {movimento_vencedor}")
        self.estado = Estado.AGUARDANDO_PROXIMA_RODADA

    def proxima_rodada(self):
        if self.estado != Estado.AGUARDANDO_PROXIMA_RODADA:
            raise ValueError("Impossível exibir resultado da rodada no estado atual")
        
        self.rodada_atual += 1
        if self.rodada_atual <= Jogo.RODADAS:
            self.estado = Estado.CONTAGEM_REGRESSIVA
        else:
            self.estado = Estado.ENCERRADO

    def exibir_resultado_final(self):
        if self.estado != Estado.ENCERRADO:
            raise ValueError("Impossível exibir resultado final no estado atual")


def looping_principal():
    jogo = Jogo()

    while True:
        if jogo.estado == Estado.NAO_INICIADO:
            jogo.iniciar_jogo()

        elif jogo.estado == Estado.CONTAGEM_REGRESSIVA:
            jogo.atualizar_contagem_regressiva()

        elif jogo.estado == Estado.PROCESSANDO_MOVIMENTO:
            jogo.processar_movimentos()

        elif jogo.estado == Estado.EXIBINDO_RESULTADO:
            jogo.exibir_resultado_rodada()

        elif jogo.estado == Estado.AGUARDANDO_PROXIMA_RODADA:
            jogo.proxima_rodada()

        elif jogo.estado == Estado.ENCERRADO:
            jogo.exibir_resultado_final()
            break

if __name__ == '__main__':
    looping_principal()
