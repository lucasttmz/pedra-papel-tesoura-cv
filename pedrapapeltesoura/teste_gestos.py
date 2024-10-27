import cv2
import mediapipe as mp

from reconhecimento import reconhecer_gesto

mp_maos = mp.solutions.hands # type: ignore
desenho = mp.solutions.drawing_utils  #type: ignore
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
            
            texto = str(reconhecer_gesto(mao.landmark))

            posicao_x = int(mao.landmark[mp_maos.HandLandmark.MIDDLE_FINGER_MCP].x * largura)
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
