import os
import shutil

def copy_multiple_images():
    # --- CONFIGURATION ---
    # Replace these paths with the actual paths on your computer.
    source_folder = r"C:\New folder\yash - Copy\100CANON"
    destination_folder = r"C:\New folder\yash - Copy\Lagna"
    # ---------------------

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: The source folder '{source_folder}' does not exist.")
        return

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        print(f"Creating destination folder: {destination_folder}")
        os.makedirs(destination_folder)

    print("--- Batch Image Copier ---")
    print("Type 'q' or 'quit' at any time to exit.")

    while True:
        # Ask the user for multiple image numbers
        user_input = input("\nEnter image numbers separated by spaces or commas (e.g., 6200 6201 6205): ").strip()

        # Exit condition
        if user_input.lower() in ['q', 'quit']:
            print("Exiting program. Goodbye!")
            break

        # Skip if they just pressed Enter by accident
        if not user_input:
            continue

        # Clean up the input: replace commas with spaces, then split into a list of numbers
        cleaned_input = user_input.replace(',', ' ')
        image_numbers = cleaned_input.split()

        print(f"\nProcessing {len(image_numbers)} images...")

        # Loop through every number the user entered
        for img_num in image_numbers:
            # Construct the exact filename
            filename = f"_MG_{img_num}.JPG"
            
            # Create full paths
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            # Check if the file exists and copy it
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, destination_path)
                    print(f"✅ Copied: {filename}")
                except Exception as e:
                    print(f"❌ Error copying {filename}: {e}")
            else:
                print(f"⚠️ Not Found: {filename} does not exist in the source folder.")

if __name__ == "__main__":
    copy_multiple_images()