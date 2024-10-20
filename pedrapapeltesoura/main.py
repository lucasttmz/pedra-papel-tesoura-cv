from jogo import Jogo
from modelos import Estado
from visualizacao import RenderTemporario


def looping_principal():
    render = RenderTemporario(0, 0, 0)
    jogo = Jogo(render)

    while True:
        if jogo.estado == Estado.NAO_INICIADO:
            jogo.iniciar_jogo()
        elif jogo.estado == Estado.CONTAGEM_REGRESSIVA:
            jogo.atualizar_contagem_regressiva()
        elif jogo.estado == Estado.PROCESSANDO_MOVIMENTO:
            jogo.processar_movimentos()
        elif jogo.estado == Estado.EXIBINDO_MOVIMENTOS:
            jogo.exibir_movimentos_detectados()
        elif jogo.estado == Estado.VERIFICANDO_VENCEDOR:
            jogo.verificar_vencedor()
        elif jogo.estado == Estado.EXIBINDO_RESULTADO:
            jogo.exibir_resultado_rodada()
        elif jogo.estado == Estado.AGUARDANDO_PROXIMA_RODADA:
            jogo.proxima_rodada()
        elif jogo.estado == Estado.ENCERRADO:
            jogo.exibir_resultado_final()
            break


if __name__ == '__main__':
    looping_principal()
