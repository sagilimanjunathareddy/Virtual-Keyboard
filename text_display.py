import cv2

def display_text(frame, text):
    cv2.rectangle(frame, (40, 30), (frame.shape[1] - 40, 80), (0, 255, 0), -1)
    display = text[-60:]  # Limit displayed chars
    cv2.putText(frame, display, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
    return frame
