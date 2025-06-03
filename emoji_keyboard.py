import cv2

emoji_keys = ["😀", "😂", "😍", "😎", "😢", "😡", "🥳", "👍", "🙏", "🔥",
              "🎉", "💯", "❤️", "🍕", "🐶", "🐱", "⚽", "🌟", "🚀", "📱"]

emoji_size = 50
emoji_per_row = 10
start_x, start_y = 80, 450

def draw_emoji_keyboard(frame):
    emoji_positions = []
    for idx, emoji in enumerate(emoji_keys):
        row = idx // emoji_per_row
        col = idx % emoji_per_row
        x = start_x + col * (emoji_size + 10)
        y = start_y + row * (emoji_size + 10)
        cv2.rectangle(frame, (x, y), (x + emoji_size, y + emoji_size), (0, 128, 255), 2)
        cv2.putText(frame, emoji, (x + 5, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 128, 255), 2)
        emoji_positions.append((emoji, (x, y, x + emoji_size, y + emoji_size)))
    return frame, emoji_positions
