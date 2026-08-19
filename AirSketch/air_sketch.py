"""
Air Canvas - Virtual Finger Drawing
------------------------------------
Draw in the air using your index finger, tracked via webcam + MediaPipe Hands.

Gestures:
  - Index finger only up   -> Draw
  - Index + Middle up      -> Selection mode (move over header to pick a
                               color, or hit CLEAR / SAVE)
  - Closed fist             -> Erase (big eraser follows your fist)
  - No hand / other poses  -> Pen up (no drawing)

Keyboard shortcuts (fallbacks for the on-screen buttons):
  c        Clear canvas
  s        Save drawing as PNG
  z        Undo last stroke
  [ / ]    Decrease / increase brush size
  q        Quit
"""

import os
import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
CAMERA_INDEX = 0
FRAME_W, FRAME_H = 1280, 720

COLORS = [
    (255, 0, 0),    # Blue
    (0, 255, 0),    # Green
    (0, 0, 255),    # Red
    (0, 255, 255),  # Yellow
    (0, 0, 0),      # Eraser
]
COLOR_NAMES = ["BLUE", "GREEN", "RED", "YELLOW", "ERASER"]

BRUSH_MIN, BRUSH_MAX = 2, 60
DEFAULT_BRUSH = 8
DEFAULT_ERASER = 50

SMOOTHING_WINDOW = 5          # higher = smoother but laggier
HEADER_HEIGHT = 65
SAVE_DIR = "air_canvas_saves"
FIST_ERASER_RADIUS = 45       # eraser size when a closed fist is detected

# --------------------------------------------------------------------------
# MediaPipe setup
# --------------------------------------------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)


def is_fist(lm_list):
    """A closed fist: index/middle/ring/pinky tips all curled below their
    PIP joints (i.e. NOT extended)."""
    index_down = lm_list[8][1] > lm_list[6][1]
    middle_down = lm_list[12][1] > lm_list[10][1]
    ring_down = lm_list[16][1] > lm_list[14][1]
    pinky_down = lm_list[20][1] > lm_list[18][1]
    return index_down and middle_down and ring_down and pinky_down


def make_buttons(width):
    """Header = color swatches + CLEAR + SAVE, evenly spaced."""
    labels = COLOR_NAMES + ["CLEAR", "SAVE"]
    n = len(labels)
    seg = width // n
    buttons = []
    for i, label in enumerate(labels):
        x0, x1 = i * seg, (i + 1) * seg if i < n - 1 else width
        color = COLORS[i] if i < len(COLORS) else (60, 60, 60)
        buttons.append({"label": label, "x0": x0, "x1": x1, "color": color})
    return buttons


def draw_header(frame, buttons, active_color, brush_size):
    for b in buttons:
        cv2.rectangle(frame, (b["x0"], 0), (b["x1"], HEADER_HEIGHT), b["color"], -1)
        text_color = (255, 255, 255) if b["color"] in [(0, 0, 0), (60, 60, 60)] else (0, 0, 0)
        cv2.putText(frame, b["label"], (b["x0"] + 10, 42),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        # Highlight the currently active color
        if b["label"] in COLOR_NAMES and COLORS[COLOR_NAMES.index(b["label"])] == active_color:
            cv2.rectangle(frame, (b["x0"], 0), (b["x1"], HEADER_HEIGHT), (255, 255, 255), 3)

    cv2.putText(frame, f"Brush: {brush_size}", (frame.shape[1] - 150, HEADER_HEIGHT + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def save_canvas(canvas):
    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = os.path.join(SAVE_DIR, f"drawing_{int(time.time())}.png")
    # Make black background transparent so only the strokes are saved
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    alpha = np.where(gray > 10, 255, 0).astype(np.uint8)
    bgra = cv2.cvtColor(canvas, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    cv2.imwrite(filename, bgra)
    return filename


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    if not cap.isOpened():
        print(f"ERROR: could not open camera index {CAMERA_INDEX}. "
              f"Check that a webcam is connected and not in use by another app.")
        return

    canvas = None
    undo_stack = deque(maxlen=15)
    point_buffer = deque(maxlen=SMOOTHING_WINDOW)

    current_color = COLORS[0]
    brush_thickness = DEFAULT_BRUSH
    eraser_thickness = DEFAULT_ERASER

    prev_x, prev_y = 0, 0
    prev_time = time.time()
    buttons = None
    last_save_msg = ""
    last_save_msg_until = 0

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("WARNING: failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            if canvas is None:
                canvas = np.zeros((h, w, 3), dtype=np.uint8)
                buttons = make_buttons(w)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            hand_detected = bool(results.multi_hand_landmarks)

            if hand_detected:
                hand_landmarks = results.multi_hand_landmarks[0]
                lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

                index_up = lm_list[8][1] < lm_list[6][1]
                middle_up = lm_list[12][1] < lm_list[10][1]

                x1, y1 = lm_list[8]
                x2, y2 = lm_list[12]

                if is_fist(lm_list):
                    # Fist mode - erase around the palm center (landmark 9
                    # is more stable than a fingertip since the fist is closed)
                    px, py = lm_list[9]
                    point_buffer.clear()
                    cv2.circle(frame, (px, py), FIST_ERASER_RADIUS, (255, 255, 255), 2)

                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = px, py
                        undo_stack.append(canvas.copy())  # snapshot before erasing

                    cv2.line(canvas, (prev_x, prev_y), (px, py), (0, 0, 0), FIST_ERASER_RADIUS * 2)
                    prev_x, prev_y = px, py

                elif index_up and middle_up:
                    # Selection mode
                    prev_x, prev_y = 0, 0
                    point_buffer.clear()
                    cv2.rectangle(frame, (x1 - 15, y1 - 15), (x2 + 15, y2 + 15), (200, 200, 200), 2)

                    if y1 < HEADER_HEIGHT:
                        for b in buttons:
                            if b["x0"] <= x1 < b["x1"]:
                                if b["label"] in COLOR_NAMES:
                                    current_color = COLORS[COLOR_NAMES.index(b["label"])]
                                elif b["label"] == "CLEAR":
                                    undo_stack.append(canvas.copy())
                                    canvas = np.zeros((h, w, 3), dtype=np.uint8)
                                elif b["label"] == "SAVE":
                                    path = save_canvas(canvas)
                                    last_save_msg = f"Saved: {path}"
                                    last_save_msg_until = time.time() + 2.5

                elif index_up and not middle_up:
                    # Drawing mode - smooth the point first
                    point_buffer.append((x1, y1))
                    sx = int(np.mean([p[0] for p in point_buffer]))
                    sy = int(np.mean([p[1] for p in point_buffer]))

                    thickness = eraser_thickness if current_color == (0, 0, 0) else brush_thickness
                    cv2.circle(frame, (sx, sy), thickness // 2, current_color, cv2.FILLED)

                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = sx, sy
                        undo_stack.append(canvas.copy())  # snapshot at stroke start

                    cv2.line(canvas, (prev_x, prev_y), (sx, sy), current_color, thickness)
                    prev_x, prev_y = sx, sy
                else:
                    prev_x, prev_y = 0, 0
                    point_buffer.clear()
            else:
                # Hand left the frame entirely -> reset so we don't draw a
                # jump line when it reappears (this was a bug in the original)
                prev_x, prev_y = 0, 0
                point_buffer.clear()

            # Merge canvas with live camera feed
            canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY_INV)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, mask)
            frame = cv2.bitwise_or(frame, canvas)

            draw_header(frame, buttons, current_color, brush_thickness)

            # FPS
            now = time.time()
            fps = 1 / max(now - prev_time, 1e-6)
            prev_time = now
            cv2.putText(frame, f"FPS: {int(fps)}", (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if last_save_msg and time.time() < last_save_msg_until:
                cv2.putText(frame, last_save_msg, (10, h - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Air Canvas - Virtual Finger Drawing", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                undo_stack.append(canvas.copy())
                canvas = np.zeros((h, w, 3), dtype=np.uint8)
            elif key == ord('s'):
                path = save_canvas(canvas)
                last_save_msg = f"Saved: {path}"
                last_save_msg_until = time.time() + 2.5
            elif key == ord('z'):
                if undo_stack:
                    canvas = undo_stack.pop()
            elif key == ord('['):
                brush_thickness = max(BRUSH_MIN, brush_thickness - 2)
            elif key == ord(']'):
                brush_thickness = min(BRUSH_MAX, brush_thickness + 2)
            elif key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    main()