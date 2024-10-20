from jogo import Jogo
from visualizacao import RenderTemporario


def looping_principal():
    render = RenderTemporario(0, 0, 0)
    jogo = Jogo(render)

    while not jogo.encerrado:
        jogo.atualizar_jogo()


if __name__ == '__main__':
    looping_principal()
