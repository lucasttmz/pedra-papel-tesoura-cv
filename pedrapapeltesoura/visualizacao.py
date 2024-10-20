from random import choice

import cv2

from constantes import Escolha, Resultado


class Janela:
    def __init__(self, sleep_contador: int = 1, sleep_movimentos: int = 3, sleep_resultado: int = 3) -> None:
        self.sleep_contador = sleep_contador
        self.sleep_movimentos = sleep_movimentos
        self.sleep_resultado = sleep_resultado
    
    def adicionar_texto(self, frame, texto: str, pos: tuple[int, int], tamanho: float):
        cv2.putText(frame, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, tamanho, (0, 0, 0), 10, cv2.LINE_AA)

    def mostrar_frame(self, frame, wait: int):
        cv2.imshow('Pedra Papel Tesoura', frame)
        cv2.waitKey(wait)
    
    def atualizar_contador(self, contagem: int, frame):
        self.adicionar_texto(frame, f"{contagem}", (250, 200), 3)
        self.mostrar_frame(frame, 1000 * self.sleep_contador)

    def ler_movimento(self, frame) -> tuple[Escolha, Escolha]:
        # TODO: Usa o frame atual no modelo de ML para detectar os movimentos
        jogador1 = choice(list(Escolha))
        jogador2 = choice(list(Escolha))
    
        return jogador1, jogador2
    
    def mostrar_movimentos(self, j1: Escolha | None, j2: Escolha | None, frame):
        movimento_j1 = j1 or "Não reconhecido"
        movimento_j2 = j2 or "Não reconhecido"
        texto = f"{movimento_j1} x {movimento_j2}"
        self.adicionar_texto(frame, texto, (30, 200), 2.5)
        self.mostrar_frame(frame, 1000 * self.sleep_movimentos)

    def mostrar_resultado(self, resultado: Resultado, escolha: Escolha | None, frame):
        if resultado == Resultado.EMPATE:
            self.adicionar_texto(frame, "Rodada Empatada!", (10, 200), 2)
        else:
            self.adicionar_texto(frame, f"Jogador {resultado} venceu", (10, 120), 2)
            self.adicionar_texto(frame, "na rodada", (130, 180), 2)
            self.adicionar_texto(frame, f"utilizando {escolha}", (60, 240), 2)
        
        self.mostrar_frame(frame, 1000 * self.sleep_resultado)

    def mostrar_resultado_final(self, resultado: Resultado, pontos_j1: int, pontos_j2: int, frame) -> None: 
        pontuacao = f"{pontos_j1} x {pontos_j2}"
        if resultado == Resultado.EMPATE:
            vencedor = "Empate!"
            x = 180
        elif pontos_j1 > pontos_j2:
            vencedor = "Jogador 1 Venceu!"
            x = 5
        else:
            vencedor = "Jogador 2 Venceu!"
            x = 5

        self.adicionar_texto(frame, vencedor, (x, 120), 2)
        self.adicionar_texto(frame, pontuacao, (180, 240), 3)
        self.mostrar_frame(frame, 1000 * self.sleep_resultado)
