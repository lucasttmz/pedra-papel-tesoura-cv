from random import choice

import cv2
import mediapipe as mp

from constantes import Escolha, Resultado
from reconhecimento import reconhecer_gesto

mp_maos = mp.solutions.hands # type: ignore
maos = mp_maos.Hands()


class Janela:
    tela_fundo = cv2.imread("ui/ui.jpg")

    def __init__(self, tamanho: tuple[int, int], contador: int = 1, movimentos: int = 3, resultado: int = 3) -> None:
        self.tamanho = tamanho
        self.sleep_contador = contador
        self.sleep_movimentos = movimentos
        self.sleep_resultado = resultado
    
    def coordenadas_para_centralizar_texto(self, texto: str, tamanho: int, espessura: int = 1):
        tamanho_texto, _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_TRIPLEX, tamanho, espessura)
        largura_texto, altura_texto = tamanho_texto
        largura, altura = self.tamanho
        posicao_x = (largura - largura_texto) // 2
        posicao_y = (altura + altura_texto) // 2  
        
        return posicao_x, posicao_y

    def adicionar_texto(self, frame, texto: str, pos: tuple[int, int], tamanho: float, cor_texto=(255,255,255), cor_borda=(0,0,0)):
        cv2.putText(frame, texto, (pos[0], pos[1]), cv2.FONT_HERSHEY_TRIPLEX, tamanho, cor_borda, 15, cv2.LINE_AA)
        cv2.putText(frame, texto, pos, cv2.FONT_HERSHEY_TRIPLEX, tamanho, cor_texto, 5, cv2.LINE_AA)

    def mostrar_frame(self, frame, wait: int):
        cv2.imshow('Pedra Papel Tesoura', frame)
        cv2.waitKey(wait)
    
    def atualizar_contador(self, contagem: int, frame):
        frame = Janela.tela_fundo.copy()
        texto = str(contagem)
        pos = self.coordenadas_para_centralizar_texto(texto, 3)

        self.adicionar_texto(frame, texto, pos, 3, (0,0,0), (255,255,255))
        self.mostrar_frame(frame, 1000 * self.sleep_contador)

    def ler_movimento(self, frame) -> tuple[Escolha | None, Escolha | None]:
        resultado = maos.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        j1, j2 = None, None
        # encontrou alguma mao
        if resultado.multi_hand_landmarks:
            # para cada mao
            for mao in resultado.multi_hand_landmarks:
                escolha = reconhecer_gesto(mao.landmark)
                if escolha and escolha[1] == Resultado.JOGADOR1:
                    j1 = escolha[0]
                elif escolha and escolha[1] == Resultado.JOGADOR2:
                    j2 = escolha[0]
                
        return j1, j2
    
    def mostrar_movimentos(self, j1: Escolha | None, j2: Escolha | None, frame):
        movimento_j1 = j1 or "Nao reconhecido"
        movimento_j2 = j2 or "Nao reconhecido"
        texto = f"{movimento_j1} x {movimento_j2}"
        pos = self.coordenadas_para_centralizar_texto(texto, 2)

        self.adicionar_texto(frame, texto, pos, 2)
        self.mostrar_frame(frame, 1000 * self.sleep_movimentos)

    def mostrar_resultado(self, resultado: Resultado, escolha: Escolha | None, frame):
        frame = Janela.tela_fundo.copy()

        if resultado == Resultado.EMPATE:
            texto = "Rodada Empatada!"
            pos = self.coordenadas_para_centralizar_texto(texto, 2)
            self.adicionar_texto(frame, texto, pos, 2, (0, 0, 255))
        else:
            texto = f"Jogador {resultado} venceu"
            x, y = self.coordenadas_para_centralizar_texto(texto, 2)
            self.adicionar_texto(frame, texto, (x, y-35), 2, (0, 255, 0))

            texto = f"utilizando {escolha}"
            x, y = self.coordenadas_para_centralizar_texto(texto, 2)
            self.adicionar_texto(frame, f"utilizando {escolha}", (x, y+35), 2)

        self.mostrar_frame(frame, 1000 * self.sleep_resultado)

    def mostrar_resultado_final(self, resultado: Resultado, pontos_j1: int, pontos_j2: int, frame) -> None:
        frame = Janela.tela_fundo.copy()

        pontuacao = f"{pontos_j1} x {pontos_j2}"
        cor_texto = (0,255,0)
        if resultado == Resultado.EMPATE:
            vencedor = "Empate!"
            cor_texto = (0,0,255)
        elif pontos_j1 > pontos_j2:
            vencedor = "Jogador 1 Venceu!"
        else:
            vencedor = "Jogador 2 Venceu!"
        
        x, y = self.coordenadas_para_centralizar_texto(vencedor, 2)
        self.adicionar_texto(frame, vencedor, (x, y-45), 2, cor_texto)

        x, y = self.coordenadas_para_centralizar_texto(pontuacao, 3)

        self.adicionar_texto(frame, pontuacao, (x, y+45), 3, cor_texto)
        self.mostrar_frame(frame, 1000 * self.sleep_resultado)
