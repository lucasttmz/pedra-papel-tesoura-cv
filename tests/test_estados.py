from pedrapapeltesoura.jogo import *


def test_estado_inicial(novo_jogo):
    assert isinstance(novo_jogo.estado_atual, EstadoNaoIniciado)


def test_estado_contagem(novo_jogo):
    for _ in range(4):
        novo_jogo.atualizar_jogo(None)
        assert isinstance(novo_jogo.estado_atual, EstadoContagemRegressiva)


def test_estado_contagem_multiplas_rodadas(novo_jogo_tres_rodadas):
    for _ in range(10):
        novo_jogo_tres_rodadas.atualizar_jogo(None)
    
    assert isinstance(novo_jogo_tres_rodadas.estado_atual, EstadoContagemRegressiva)


def test_estado_processamento_movimentos(novo_jogo):
    for _ in range(5):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoProcessandoMovimento)


def test_estado_exibindo_movimentos(novo_jogo):
    for _ in range(6):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoExibindoMovimentos)


def test_estado_verificando_vencedor(novo_jogo):
    for _ in range(7):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoVerificandoVencedor)


def test_estado_exibindo_resultado(novo_jogo):
    for _ in range(8):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoExibindoResultado)


def test_estado_aguardando_rodada(novo_jogo):
    for _ in range(9):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoAguardandoProximaRodada)


def test_estado_encerrado(novo_jogo):
    for _ in range(10):
        novo_jogo.atualizar_jogo(None)
    
    assert isinstance(novo_jogo.estado_atual, EstadoEncerrado)


def test_estado_encerrado_como_final(novo_jogo):
    while not novo_jogo.encerrado:
        novo_jogo.atualizar_jogo(None)

    assert isinstance(novo_jogo.estado_atual, EstadoEncerrado)
