"""
Hand Frame Filter
------------------
Pinch your thumb and index finger together on EACH hand. The midpoint
between thumb tip and index tip (the "pinch point") becomes that hand's
rectangle corner - two hands pinching gives you two opposite corners,
and a live video filter is applied ONLY inside that rectangle. Everything
outside the rectangle stays normal camera feed.

Requires both hands visible to draw/apply the filter; with 0 or 1 hand
visible, you just see the plain camera feed.

Keyboard shortcuts:
  1        Grayscale
  2        Gaussian blur
  3        Canny edge detection
  4        Invert colors
  5        Sepia tone
  6        Pixelate
  7        Thermal (JET colormap)
  n / p    Next / previous filter
  q        Quit
"""

import time

import cv2
import mediapipe as mp
import numpy as np

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
CAMERA_INDEX = 0
FRAME_W, FRAME_H = 1280, 720
MIN_BOX_SIZE = 20          # ignore degenerate rectangles smaller than this
PIXELATE_BLOCKS = 12       # lower = chunkier pixelation

# --------------------------------------------------------------------------
# MediaPipe setup
# --------------------------------------------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

THUMB_TIP = 4
INDEX_TIP = 8


# --------------------------------------------------------------------------
# Filters - each takes a BGR ROI and returns a BGR image of the same shape
# --------------------------------------------------------------------------
def f_grayscale(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def f_blur(roi):
    return cv2.GaussianBlur(roi, (25, 25), 0)


def f_edges(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 150)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def f_invert(roi):
    return cv2.bitwise_not(roi)


def f_sepia(roi):
    kernel = np.array([[0.272, 0.534, 0.131],
                        [0.349, 0.686, 0.168],
                        [0.393, 0.769, 0.189]])
    sepia = cv2.transform(roi, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)


def f_pixelate(roi):
    h, w = roi.shape[:2]
    if h < 1 or w < 1:
        return roi
    small = cv2.resize(roi, (max(1, w // PIXELATE_BLOCKS), max(1, h // PIXELATE_BLOCKS)),
                        interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def f_thermal(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)


FILTERS = [
    ("Grayscale", f_grayscale),
    ("Blur", f_blur),
    ("Edges", f_edges),
    ("Invert", f_invert),
    ("Sepia", f_sepia),
    ("Pixelate", f_pixelate),
    ("Thermal", f_thermal),
]


def get_pinch_points(results, w, h):
    """Return a list of dicts with each hand's pinch midpoint (corner) plus
    the raw thumb/index tip positions, used for visual feedback."""
    points = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            t = hand_landmarks.landmark[THUMB_TIP]
            i = hand_landmarks.landmark[INDEX_TIP]
            thumb = (int(t.x * w), int(t.y * h))
            index = (int(i.x * w), int(i.y * h))
            mid = ((thumb[0] + index[0]) // 2, (thumb[1] + index[1]) // 2)
            points.append({"thumb": thumb, "index": index, "mid": mid})
    return points


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    if not cap.isOpened():
        print(f"ERROR: could not open camera index {CAMERA_INDEX}. "
              f"Check that a webcam is connected and not in use by another app.")
        return

    filter_idx = 0
    prev_time = time.time()

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("WARNING: failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            pinches = get_pinch_points(results, w, h)

            # Visual feedback: line between thumb/index + dot at the pinch midpoint
            for p in pinches:
                cv2.line(frame, p["thumb"], p["index"], (0, 255, 255), 2)
                cv2.circle(frame, p["thumb"], 6, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, p["index"], 6, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, p["mid"], 8, (0, 255, 255), cv2.FILLED)

            tips = [p["mid"] for p in pinches]

            if len(tips) >= 2:
                (x1, y1), (x2, y2) = tips[0], tips[1]
                x_min, x_max = sorted((x1, x2))
                y_min, y_max = sorted((y1, y2))

                # Clip to frame bounds
                x_min, x_max = max(0, x_min), min(w, x_max)
                y_min, y_max = max(0, y_min), min(h, y_max)

                if (x_max - x_min) >= MIN_BOX_SIZE and (y_max - y_min) >= MIN_BOX_SIZE:
                    roi = frame[y_min:y_max, x_min:x_max]
                    name, filt_fn = FILTERS[filter_idx]
                    filtered = filt_fn(roi)
                    frame[y_min:y_max, x_min:x_max] = filtered

                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x_min, max(20, y_min - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # HUD
            now = time.time()
            fps = 1 / max(now - prev_time, 1e-6)
            prev_time = now
            cv2.putText(frame, f"FPS: {int(fps)}", (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Filter: {FILTERS[filter_idx][0]} (1-7, n/p)",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            if len(tips) < 2:
                cv2.putText(frame, "Pinch thumb + index on both hands to frame a rectangle",
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2)

            cv2.imshow("Hand Frame Filter", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key in [ord(str(i)) for i in range(1, 8)]:
                filter_idx = int(chr(key)) - 1
            elif key == ord('n'):
                filter_idx = (filter_idx + 1) % len(FILTERS)
            elif key == ord('p'):
                filter_idx = (filter_idx - 1) % len(FILTERS)

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    main()