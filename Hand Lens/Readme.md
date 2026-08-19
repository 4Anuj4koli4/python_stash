# HandLens 🖼️👐

Frame a rectangle between your two hands and watch a live video filter appear only inside it. HandLens uses [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) to track a pinch point on each hand — the two pinch points become opposite corners of a rectangle, and everything inside gets filtered in real time while the rest of the feed stays normal.

## Features

- **Two-hand rectangle framing** — pinch thumb + index finger on each hand to set the rectangle's corners
- **7 live filters** — grayscale, blur, edge detection, invert, sepia, pixelate, and thermal (JET colormap)
- **Instant filter switching** — number keys or next/previous cycling, no restart needed
- **Visual pinch feedback** — see the thumb-index connector line and pinch point on each hand
- **Live FPS counter** — track performance in real time

## Requirements

- Python 3.8+
- A webcam
- Packages: `opencv-python`, `mediapipe`, `numpy`

```bash
pip install opencv-python mediapipe numpy
```

## Usage

```bash
python hand_frame_filter.py
```

A window opens with your live camera feed. Pinch thumb and index finger on **both** hands to frame a rectangle — the filtered region appears immediately.

## Gestures

| Gesture                       | Action                                                                                   |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| 🤏 Pinch on one hand          | Marks that hand's pinch point (visible as a yellow dot)                                  |
| 🤏🤏 Pinch on both hands      | Forms a rectangle between the two pinch points — the current filter is applied inside it |
| 🖐️ Fewer than 2 hands visible | No rectangle, no filter — plain camera feed                                              |

## Keyboard Shortcuts

| Key     | Action                                                                               |
| ------- | ------------------------------------------------------------------------------------ |
| `1`–`7` | Jump directly to a filter (Grayscale, Blur, Edges, Invert, Sepia, Pixelate, Thermal) |
| `n`     | Next filter                                                                          |
| `p`     | Previous filter                                                                      |
| `q`     | Quit                                                                                 |

## How it works

Each frame, MediaPipe detects up to 2 hands and their 21 landmarks each. HandLens takes the thumb tip and index tip of every detected hand, computes the midpoint between them (the "pinch point"), and — when two hands are visible — uses those two points as opposite corners of a rectangle. The selected filter function is applied only to the pixels inside that rectangle before the frame is displayed, so the effect updates live as you move your hands.

## Known limitations

- Requires both hands to be visible simultaneously to form a rectangle
- Very small rectangles (below `MIN_BOX_SIZE`) are ignored to avoid errors on degenerate regions
- Filter is reapplied fresh each frame — it does not persist once your hands leave the frame
- Works best in good, even lighting so MediaPipe can track hand landmarks reliably
