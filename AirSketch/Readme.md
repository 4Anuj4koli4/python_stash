# AirSketch ✋🎨

Draw in thin air using nothing but your webcam and your hand. AirSketch tracks your fingertip with [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) and turns hand gestures into a real-time drawing canvas overlaid on your live camera feed.

## Features

- **Finger drawing** — draw with your index finger, no mouse or stylus needed
- **Gesture-based color picker** — hold up index + middle finger and hover over the on-screen header to pick a color
- **Fist to erase** — make a closed fist to erase; a bigger eraser circle follows your fist
- **Undo** — step back through your last 15 strokes
- **Save your art** — export your drawing as a transparent PNG
- **Adjustable brush size** — grow or shrink your brush on the fly
- **Jitter smoothing** — averages recent points so lines come out steady, not shaky
- **Live FPS counter** — see your tracking performance in real time

## Requirements

- Python 3.8+
- A webcam
- Packages: `opencv-python`, `mediapipe`, `numpy`

```bash
pip install opencv-python mediapipe numpy
```

## Usage

```bash
python air_canvas.py
```

A window will open showing your live camera feed with a color header at the top. Use the gestures below to draw, pick colors, erase, and save.

## Gestures

| Gesture                      | Action                                                                     |
| ---------------------------- | -------------------------------------------------------------------------- |
| ☝️ Index finger only, up     | Draw                                                                       |
| ✌️ Index + middle finger, up | Selection mode — hover over the header to pick a color or hit CLEAR / SAVE |
| ✊ Closed fist               | Erase — a big eraser follows your fist                                     |
| 🖐️ No hand / other pose      | Pen up — nothing happens                                                   |

## Keyboard Shortcuts

| Key       | Action                         |
| --------- | ------------------------------ |
| `c`       | Clear canvas                   |
| `s`       | Save drawing as PNG            |
| `z`       | Undo last stroke               |
| `[` / `]` | Decrease / increase brush size |
| `q`       | Quit                           |

Saved drawings land in an `air_canvas_saves/` folder created next to the script, named `drawing_<timestamp>.png` with a transparent background (only your strokes are kept — the black canvas background is stripped out).

## How it works

Each frame, MediaPipe detects your hand's 21 landmarks. AirSketch checks which fingers are extended to decide the current mode (draw / select / erase), then either draws onto an invisible canvas layer or applies UI actions. The canvas is merged with the live camera frame every frame using a black-pixel mask, so your strokes appear to float over the video feed.

## Known limitations

- Single-hand tracking only
- The eraser works by drawing black onto the canvas, so it assumes a black canvas background — it isn't a true "hole" in the drawing until you save (where black becomes transparent)
- Works best in good, even lighting so MediaPipe can track hand landmarks reliably
