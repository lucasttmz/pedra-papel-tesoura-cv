"""
Script para testar o reconhecimento das mãos
"""

import cv2
import mediapipe as mp

from reconhecimento import reconhecer_gesto
from constantes import Jogadores

mp_maos = mp.solutions.hands
desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands()

webcam = cv2.VideoCapture(0)
while True:
    sucesso, frame = webcam.read()
    if not sucesso:
        break

    # processa as maos
    resultado = maos.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    altura, largura, _ = frame.shape
    
    if resultado.multi_hand_landmarks:
        for mao in resultado.multi_hand_landmarks:
            
            reconhecido = reconhecer_gesto(mao.landmark)
            texto = str(reconhecido)

            posicao_x = int(mao.landmark[mp_maos.HandLandmark.MIDDLE_FINGER_MCP].x * largura)
            if reconhecido and reconhecido[1] == Jogadores.JOGADOR2:
                posicao_x -= 300
            posicao_y = int(mao.landmark[mp_maos.HandLandmark.MIDDLE_FINGER_MCP].y * altura)

            cv2.putText(
                frame, texto, 
                (posicao_x, posicao_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA
            )


    cv2.imshow('Pedra, Papel e Tesoura', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
