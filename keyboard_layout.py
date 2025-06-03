import cv2

key_width = 35
key_height = 35
offset_x = 40
offset_y = 100

rows = [
    ["ESC", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACK"],
    ["TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["CAPS", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
    ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "SHIFT"],
    ["SPACE"]
]

def draw_keyboard(frame):
    key_positions = []
    for row_index, row in enumerate(rows):
        x = offset_x
        y = offset_y + row_index * (key_height + 10)

        for key in row:
            width = key_width
            if key in ["TAB", "CAPS", "SHIFT"]:
                width *= 1.5
            elif key == "ENTER":
                width *= 2
            elif key == "SPACE":
                width *= 6
            elif key == "BACK":
                width *= 2

            x2 = int(x + width)
            y2 = int(y + key_height)

            cv2.rectangle(frame, (int(x), y), (x2, y2), (255, 0, 0), 2)
            font_scale = 0.7 if len(key) > 1 else 0.8
            text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
            text_x = int(x + (width - text_size[0]) / 2)
            text_y = int(y + (key_height + text_size[1]) / 2)
            cv2.putText(frame, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)

            key_positions.append((key, (int(x), y, x2, y2)))
            x += width + 5
    return frame, key_positions
