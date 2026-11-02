# تعداد انگشتان باز کد های هوش مصنوعی
import cv2
import mediapipe as mp

mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
draw_util = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
finger_counter = 0
finger_tips = [8, 12 , 16, 20]
while True:

    finger_counter = 0
    success , frame = cap.read()
    if not success:
        break

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            landmark = hand.landmark
            # draw_util.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            for tip in finger_tips:
                if landmark[tip].y < landmark[tip-2].y:
                    finger_counter +=1
            if landmark[4].x > landmark[3].x:
                finger_counter +=1
                   
    # این خط رنگ تصویر رو برای نمایش درست می‌کنه
    frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)

    cv2.putText(frame, str(finger_counter), (50, 100), cv2.FONT_HERSHEY_COMPLEX,
                3, (0, 255, 0), 3)


    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
