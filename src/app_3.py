#کد استاد مشکل داره 
#کد علامت پیروزی
import cv2
import mediapipe as mp

mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
finger_counter_open = 0
finger_counter_close = 0
victory_sign = ''
finger_tips_open = [8, 12]
finger_tips_close = [16, 20]
while True:

    finger_counter_open = 0
    finger_counter_close = 0
    success , frame = cap.read()
    if not success:
        break

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            landmark = hand.landmark
            # draw_util.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            for tip in finger_tips_open:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_counter_open +=1

            for tip in finger_tips_close:
                if landmark[tip].y > landmark[tip-2].y:
                    finger_counter_close +=1

            if landmark[4].x < landmark[3].x:
                finger_counter_close +=1

            if finger_counter_open == 2 and finger_counter_close ==3:
                victory_sign = 'VICTORY'
            else:
                victory_sign = 'NOT VICTORY'
    cv2.putText(frame, victory_sign, (50, 100), cv2.FONT_HERSHEY_COMPLEX,
                3, (0, 255, 0), 3)


    frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()