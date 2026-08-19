# Batch Photo Copier 📸

A quick command-line tool for picking out the good shots from a DSLR memory card without manually hunting through folders. Type in the photo numbers you want, and it copies them straight to your destination folder.

## Why

Going through hundreds of shots on a memory card and dragging out the keepers one by one is slow. This script lets you jot down the numbers of the photos you liked (e.g. while reviewing on your camera or a preview app) and copy them all in one go.

## Requirements

- Python 3.x (uses only built-in `os` and `shutil` — no installs needed)

## Setup

Open the script and update these two paths for your setup:

```python
source_folder = r"C:\New folder\yash - Copy\100CANON"
destination_folder = r"C:\New folder\yash - Copy\Lagna"
```

## Usage

```bash
python copy_photos.py
```

Then enter the photo numbers you want, separated by spaces or commas:

```
Enter image numbers separated by spaces or commas (e.g., 6200 6201 6205): 6203, 6210 6215
```

Each number is matched to a file named `_MG_<number>.JPG` in the source folder and copied to the destination. Type `q` or `quit` to exit.

## Notes

- Expects the DSLR's default filename pattern `_MG_####.JPG` — update the `filename` line in the script if your camera names files differently (e.g. `DSC_####.JPG`, `IMG_####.JPG`)
- Skips and warns about any number that doesn't match a file, so typos don't stop the batch
- Destination folder is created automatically if it doesn't already exist