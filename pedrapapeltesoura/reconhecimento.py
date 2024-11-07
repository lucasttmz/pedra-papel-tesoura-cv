"""
Lógica de reconhecimento das mãos
"""

import mediapipe as mp

from constantes import Escolha, Jogadores


def reconhecer_gesto(landmarks) -> tuple[Escolha, Jogadores] | None:
    indicador_ponta = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    indicador_meio = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]
    polegar_ponta = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
    polegar_meio = landmarks[mp.solutions.hands.HandLandmark.THUMB_IP]
    dedo_meio_ponta = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    dedo_meio_meio = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP]
    anelar_ponta = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    anelar_meio = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_PIP]
    mindinho_ponta = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]
    mindinho_meio = landmarks[mp.solutions.hands.HandLandmark.PINKY_PIP]
    punho = landmarks[mp.solutions.hands.HandLandmark.WRIST]

    # Verificacao do polegar (mão na posição correta)
    if indicador_meio.y < mindinho_meio.y:
        polegar_estendido = polegar_ponta.y < polegar_meio.y
    # Para o caso da mão estar de ponta cabeça
    else:
        polegar_estendido = polegar_ponta.y > polegar_meio.y

    # Verificação do jogador 1 (apontando para a direita)
    if punho.x < indicador_ponta.x:
        if (indicador_ponta.x > indicador_meio.x and dedo_meio_ponta.x > dedo_meio_meio.x and 
            anelar_ponta.x > anelar_meio.x and mindinho_ponta.x > mindinho_meio.x and 
            polegar_estendido):
            return Escolha.PAPEL, Jogadores.JOGADOR1
        elif (indicador_ponta.x > indicador_meio.x and dedo_meio_ponta.x > dedo_meio_meio.x and
            anelar_ponta.x <= anelar_meio.x and mindinho_ponta.x <= mindinho_meio.x and
            not polegar_estendido):
            return Escolha.TESOURA, Jogadores.JOGADOR1
        elif (indicador_ponta.x <= indicador_meio.x and dedo_meio_ponta.x <= dedo_meio_meio.x and 
            anelar_ponta.x <= anelar_meio.x and mindinho_ponta.x <= mindinho_meio.x and
            not polegar_estendido):
            return Escolha.PEDRA, Jogadores.JOGADOR1
    # Verificação do jogador 2 (apontando para a esquerda)
    else:
        if (indicador_ponta.x < indicador_meio.x and dedo_meio_ponta.x < dedo_meio_meio.x and 
            anelar_ponta.x < anelar_meio.x and mindinho_ponta.x < mindinho_meio.x and
            polegar_estendido):
            return Escolha.PAPEL, Jogadores.JOGADOR2
        elif (indicador_ponta.x < indicador_meio.x and dedo_meio_ponta.x < dedo_meio_meio.x and
            anelar_ponta.x >= anelar_meio.x and mindinho_ponta.x >= mindinho_meio.x and
            not polegar_estendido):
            return Escolha.TESOURA, Jogadores.JOGADOR2
        elif (indicador_ponta.x >= indicador_meio.x and dedo_meio_ponta.x >= dedo_meio_meio.x and 
            anelar_ponta.x >= anelar_meio.x and mindinho_ponta.x >= mindinho_meio.x and
            not polegar_estendido):
            return Escolha.PEDRA, Jogadores.JOGADOR2

    # Se chegar aqui, não reconheceu nenhum gesto
    return None
