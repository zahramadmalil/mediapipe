# کد علامت پیروزی هوش مصنوعی

import cv2
import mediapipe as mp

mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
finger_tips_open = [8, 12]
finger_tips_close = [16, 20]

while True:
    finger_counter_open = 0
    finger_counter_close = 0
    victory_sign = 'NO HAND'
    
    success, frame = cap.read()
    if not success:
        break

    # 1. تبدیل به RGB برای mediapipe
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 2. پردازش با mediapipe
    result = mp_hand.process(frameRGB)

    # 3. بررسی دست
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmark = hand.landmark

            for tip in finger_tips_open:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_counter_open += 1

            for tip in finger_tips_close:
                if landmark[tip].y > landmark[tip-2].y:
                    finger_counter_close += 1

            if landmark[4].x < landmark[3].x:
                finger_counter_close += 1

            if finger_counter_open == 2 and finger_counter_close == 3:
                victory_sign = 'VICTORY'
            else:
                victory_sign = 'NOT VICTORY'

    # 4. نمایش متن روی frame اصلی (BGR)
    cv2.putText(frame, victory_sign, (50, 100), cv2.FONT_HERSHEY_COMPLEX,
                3, (0, 255, 0), 3)

    # 5. نمایش frame اصلی (BGR) - نیازی به تبدیل نیست
    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()