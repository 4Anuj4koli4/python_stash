"""
Background Remover
-------------------
Removes the background from an image (or a whole folder of images) using
the `rembg` library, and saves the result as a transparent PNG.

Usage:
    python remove_background.py path/to/image.jpg
    python remove_background.py path/to/image.jpg -o path/to/output.png
    python remove_background.py path/to/folder --batch
    python remove_background.py path/to/folder --batch -o path/to/output_folder
"""

import argparse
import os
import sys

from rembg import remove, new_session
from PIL import Image

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
DEFAULT_MODEL = "u2netp"  # small (~4MB), fast, good for everyday photos


def remove_background(input_path: str, output_path: str, session) -> None:
    """Remove the background from a single image and save it as a PNG."""
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    output_bytes = remove(input_bytes, session=session)

    with open(output_path, "wb") as f:
        f.write(output_bytes)


def make_output_path(input_path: str, output_arg: str, is_batch: bool, output_dir_for_batch: str = None) -> str:
    """Work out where to save the result, always as .png (needed for transparency)."""
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    if is_batch:
        out_dir = output_dir_for_batch or (os.path.dirname(input_path) + "_no_bg")
        os.makedirs(out_dir, exist_ok=True)
        return os.path.join(out_dir, f"{base_name}.png")

    if output_arg:
        return output_arg

    return os.path.join(os.path.dirname(input_path), f"{base_name}_no_bg.png")


def process_single(input_path: str, output_arg: str, session) -> None:
    if not os.path.exists(input_path):
        print(f"Error: '{input_path}' does not exist.")
        sys.exit(1)

    output_path = make_output_path(input_path, output_arg, is_batch=False)

    print(f"Processing: {input_path}")
    try:
        remove_background(input_path, output_path, session)
        print(f"✅ Saved: {output_path}")
    except Exception as e:
        print(f"❌ Failed to process {input_path}: {e}")
        sys.exit(1)


def process_batch(input_dir: str, output_arg: str, session) -> None:
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a valid folder.")
        sys.exit(1)

    files = [
        f for f in sorted(os.listdir(input_dir))
        if f.lower().endswith(SUPPORTED_EXTENSIONS)
    ]

    if not files:
        print(f"No supported images found in '{input_dir}'.")
        return

    print(f"Found {len(files)} image(s) to process.\n")

    success_count = 0
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = make_output_path(input_path, None, is_batch=True, output_dir_for_batch=output_arg)

        print(f"Processing: {filename}")
        try:
            remove_background(input_path, output_path, session)
            print(f"✅ Saved: {output_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

    print(f"\nDone. {success_count}/{len(files)} image(s) processed successfully.")


def main():
    parser = argparse.ArgumentParser(description="Remove the background from image(s).")
    parser.add_argument("input", help="Path to an image file, or a folder if using --batch")
    parser.add_argument("-o", "--output", help="Output file path (single mode) or output folder (batch mode)")
    parser.add_argument("--batch", action="store_true", help="Process every image in the given folder")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"rembg model to use (default: {DEFAULT_MODEL}). "
             f"Try 'u2net' for better quality on people/objects, or 'bria-rmbg' for the highest quality (large download).",
    )
    args = parser.parse_args()

    print(f"Loading model '{args.model}' (first run downloads it, may take a moment)...")
    session = new_session(args.model)

    if args.batch:
        process_batch(args.input, args.output, session)
    else:
        process_single(args.input, args.output, session)


if __name__ == "__main__":
    main()