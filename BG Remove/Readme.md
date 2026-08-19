# Background Remover 🖼️✂️

Removes the background from an image (or a whole folder of them) and saves the result as a transparent PNG. Powered by [`rembg`](https://github.com/danielgatis/rembg), which runs a neural network locally — no external API, no upload.

## Features

- **Single image or batch mode** — process one file or an entire folder
- **Transparent PNG output** — ready to drop onto any background
- **Choice of model** — fast/lightweight by default, with the option to switch to a higher-quality (larger) model
- **Clear progress and error messages** per file

## Requirements

- Python 3.8+
- Packages: `rembg`, `pillow`

```bash
pip install rembg pillow
```

The first time you run the script, it downloads the model file automatically (a few MB for the default model). This needs an internet connection once — after that, it's cached locally and works offline.

## Usage

**Single image:**

```bash
python remove_background.py photo.jpg
```

Saves `photo_no_bg.png` next to the original.

**Custom output path:**

```bash
python remove_background.py photo.jpg -o result.png
```

**Whole folder (batch mode):**

```bash
python remove_background.py my_photos --batch
```

Saves everything into a new `my_photos_no_bg/` folder.

**Batch with custom output folder:**

```bash
python remove_background.py my_photos --batch -o cleaned_photos
```

**Using a different model:**

```bash
python remove_background.py photo.jpg --model u2net
```

## Models

| Model              | Size    | Notes                                                   |
| ------------------ | ------- | ------------------------------------------------------- |
| `u2netp` (default) | ~4 MB   | Fast, small download, good for quick everyday use       |
| `u2net`            | ~176 MB | Better quality, especially on people                    |
| `bria-rmbg`        | ~1 GB   | Highest quality, large download and more RAM/CPU needed |

Pick with `--model <name>`. Stick with the default unless you need sharper edges on complex subjects.

## Supported input formats

`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`

## Notes

- Output is always saved as `.png` (needed to preserve transparency)
- In batch mode, non-image files in the folder are skipped automatically
- Processing time depends on the model chosen and your CPU — the default model is fast even on modest hardware
