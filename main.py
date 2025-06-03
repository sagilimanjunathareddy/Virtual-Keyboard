import cv2
import mediapipe as mp
import time

from utils.keyboard_layout import draw_keyboard
from utils.gesture_utils import is_pinch
from utils.text_display import display_text

typed_text = ""
cooldown = 0
pressed_key = None
pressed_time = 0
caps_lock = False
shift_active = False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


with mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                    min_detection_confidence=0.7, min_tracking_confidence=0.6) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        frame, key_positions = draw_keyboard(frame)
        frame = display_text(frame, typed_text)

        index_fingers = []
        thumbs = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark
                index_fingers.append((int(landmarks[8].x * w), int(landmarks[8].y * h)))
                thumbs.append((landmarks[4].x, landmarks[4].y))

        hover_key = None
        if index_fingers:
            for idx, (ix, iy) in enumerate(index_fingers):
                pinch = is_pinch(index_fingers[idx], thumbs[idx])
                for key, (x1, y1, x2, y2) in key_positions:
                    if x1 <= ix <= x2 and y1 <= iy <= y2:
                        hover_key = key
                        if not pinch:
                            overlay = frame.copy()
                            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 255), -1)
                            alpha = 0.4
                            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
                        break

        if cooldown > 0:
            cooldown -= 1

        if hover_key and pinch and cooldown == 0:
            key = hover_key
            if key == "BACK":
                typed_text = typed_text[:-1]
            elif key == "SPACE":
                typed_text += " "
            elif key == "ENTER":
                typed_text += "\n"
            elif key == "CAPS":
                caps_lock = not caps_lock
            elif key == "SHIFT":
                shift_active = True
            else:
                char = key
                if len(char) == 1 and char.isalpha():
                    if caps_lock ^ shift_active:
                        char = char.upper()
                    else:
                        char = char.lower()
                elif shift_active:
                    shifted = {
                        "`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%",
                        "6": "^", "7": "&", "8": "*", "9": "(", "0": ")",
                        "-": "_", "=": "+", "[": "{", "]": "}", "\\": "|",
                        ";": ":", "'": "\"", ",": "<", ".": ">", "/": "?"
                    }
                    char = shifted.get(char, char)
                typed_text += char
                shift_active = False

            cooldown = 15
            pressed_key = key
            pressed_time = time.time()

        cv2.imshow("Gesture Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
