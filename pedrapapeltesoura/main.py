"""
Ponto de entrada da aplicação
"""

import cv2

from jogo import Jogo
from visualizacao import Janela


def looping_principal():
    jogo = Jogo(Janela((1280, 720)), rodadas=3)
    webcam = cv2.VideoCapture(0)

    while True:
        sucesso, frame = webcam.read()
        if not sucesso:
            break

        if not jogo.encerrado:
            jogo.atualizar_jogo(frame)
        elif cv2.waitKey(0):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    looping_principal()
