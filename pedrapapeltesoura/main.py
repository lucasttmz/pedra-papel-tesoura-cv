import cv2
import numpy as np

from jogo import Jogo
from visualizacao import Janela


def looping_principal():
    jogo = Jogo(Janela())

    while True:
        # Frame temporário (todo branco)
        frame = np.ones((400, 600, 3), dtype=np.uint8) * 255 

        if not jogo.encerrado:
            jogo.atualizar_jogo(frame)
        else:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    looping_principal()
