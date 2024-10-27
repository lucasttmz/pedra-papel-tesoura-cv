import mediapipe as mp

from constantes import Escolha, Resultado

def reconhecer_gesto(landmarks) -> tuple[Escolha, Resultado] | None:
    indicador_ponta = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP] # type: ignore
    indicador_meio = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP] # type: ignore
    polegar_ponta = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP] # type: ignore
    polegar_meio = landmarks[mp.solutions.hands.HandLandmark.THUMB_MCP] # type: ignore
    dedo_meio_ponta = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP] # type: ignore
    dedo_meio_meio = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP] # type: ignore
    anelar_ponta = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP] # type: ignore
    anelar_meio = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_PIP] # type: ignore
    mindinho_ponta = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP] # type: ignore
    mindinho_meio = landmarks[mp.solutions.hands.HandLandmark.PINKY_PIP] # type: ignore
    punho = landmarks[mp.solutions.hands.HandLandmark.WRIST] # type: ignore

    if punho.x < indicador_ponta.x:
        if (indicador_ponta.x > indicador_meio.x and dedo_meio_ponta.x > dedo_meio_meio.x and 
            anelar_ponta.x > anelar_meio.x and mindinho_ponta.x > mindinho_meio.x):
            return Escolha.PAPEL, Resultado.JOGADOR1
        elif indicador_ponta.x > indicador_meio.x and dedo_meio_ponta.x > dedo_meio_meio.x:
            return Escolha.TESOURA, Resultado.JOGADOR1
        elif (indicador_ponta.x <= indicador_meio.x and dedo_meio_ponta.x <= dedo_meio_meio.x and 
            anelar_ponta.x <= anelar_meio.x and mindinho_ponta.x <= mindinho_meio.x and
            (polegar_ponta.y * 720 + 25) >= (polegar_meio.y * 720)):
            return Escolha.PEDRA, Resultado.JOGADOR1
    else:
        if (indicador_ponta.x < indicador_meio.x and dedo_meio_ponta.x < dedo_meio_meio.x and 
            anelar_ponta.x < anelar_meio.x and mindinho_ponta.x < mindinho_meio.x):
            return Escolha.PAPEL, Resultado.JOGADOR2
        elif indicador_ponta.x < indicador_meio.x and dedo_meio_ponta.x < dedo_meio_meio.x:
            return Escolha.TESOURA, Resultado.JOGADOR2
        elif (indicador_ponta.x >= indicador_meio.x and dedo_meio_ponta.x >= dedo_meio_meio.x and 
            anelar_ponta.x >= anelar_meio.x and mindinho_ponta.x >= mindinho_meio.x and
            (polegar_ponta.y * 720 + 25) >= (polegar_meio.y * 720)):
            return Escolha.PEDRA, Resultado.JOGADOR2

    return None
