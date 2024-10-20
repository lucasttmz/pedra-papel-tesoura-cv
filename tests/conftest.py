from unittest.mock import patch

import pytest

from pedrapapeltesoura.jogo import Jogo
from pedrapapeltesoura.visualizacao import Janela


@pytest.fixture
def janela_mock():
    with patch.multiple(
        Janela,
        atualizar_contador=lambda *args: None,
        ler_movimento=lambda *args: ("tesoura", "pedra"),
        mostrar_movimentos=lambda *args: None,
        mostrar_resultado=lambda *args: None,
        mostrar_resultado_final=lambda *args: None,
    ):
        yield Janela()


@pytest.fixture
def novo_jogo(janela_mock):
    return Jogo(janela_mock, 1)

@pytest.fixture
def novo_jogo_tres_rodadas(janela_mock):
    return Jogo(janela_mock, 3)
