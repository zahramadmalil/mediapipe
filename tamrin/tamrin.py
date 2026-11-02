import cv2
import mediapipe as mp
import pygame
import time


pygame.mixer.init()
pygame.mixer.music.load("bikalam.mp3")
pygame.mixer.music.play(-1)


mp_hand = mp.solutions.hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

finger_tips = [8, 12, 16, 20]

current_volume = 0.5
pygame.mixer.music.set_volume(current_volume)


down_pattern = False
down_step = 0


up_pattern = False
up_step = 0

last_detection_time = 0

def detect_fingers(landmarks):
    count = 0
    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            count += 1
    
    return count

while True:
    success, frame = cap.read()
    if not success:
        break

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_hand.process(frameRGB)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            landmark = hand.landmark
            finger_count = detect_fingers(landmark)

    now = time.time()

    
    if finger_count == 3 and down_step == 0 and not up_pattern:
        down_pattern = True
        down_step = 1
        last_detection_time = now

    elif down_pattern and finger_count == 2 and down_step == 1:
        down_step = 2
        last_detection_time = now

    elif down_pattern and finger_count == 1 and down_step == 2:
        
        current_volume = max(0.0, current_volume - 0.1)
        pygame.mixer.music.set_volume(current_volume)
        down_pattern = False
        down_step = 0
        last_detection_time = now

    
    if finger_count == 1 and up_step == 0 and not down_pattern:
        up_pattern = True
        up_step = 1
        last_detection_time = now

    elif up_pattern and finger_count == 2 and up_step == 1:
        up_step = 2
        last_detection_time = now

    elif up_pattern and finger_count == 3 and up_step == 2:
        
        current_volume = min(1.0, current_volume + 0.1)
        pygame.mixer.music.set_volume(current_volume)
        up_pattern = False
        up_step = 0
        last_detection_time = now

    
    if (down_pattern or up_pattern) and (now - last_detection_time > 3):
        down_pattern = False
        down_step = 0
        up_pattern = False
        up_step = 0

    
    frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)
    cv2.putText(frame, f"Fingers: {finger_count}", (30, 60),
                cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 0), 2)
    cv2.putText(frame, f"Volume: {current_volume:.1f}", (30, 120),
                cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 0), 2)
    cv2.imshow('WebCam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()