import os
import numpy as np

def compute_and_save_histogram(raw_filename, bin_filename, width=1920, height=1080, num_bins=1024):
    """
    Reads a 16-bit raw image, computes the histogram, and saves it as a .bin file.

    Parameters:
        raw_filename (str): Path to the raw image file.
        bin_filename (str): Path to save the histogram bin file.
        width (int): Image width.
        height (int): Image height.
        num_bins (int): Number of histogram bins (1024 for 10-bit images).
    """
    try:
        # Read the raw image
        with open(raw_filename, "rb") as f:
            raw_data = np.frombuffer(f.read(), dtype=np.uint16)

        # Ensure the data matches expected size
        if raw_data.size != width * height:
            raise ValueError(f"Unexpected image size in {raw_filename}. Expected {width * height}, got {raw_data.size}")

        # Reshape to expected image dimensions
        image = raw_data.reshape((height, width))

        # Compute histogram (10-bit values range from 0 to 1023)
        histogram, _ = np.histogram(image, bins=num_bins, range=(0, 1023))

        # Save histogram as a binary file (32-bit integers)
        with open(bin_filename, "wb") as f:
            f.write(histogram.astype(np.uint32).tobytes())

        print(f"Saved histogram: {bin_filename}")

    except Exception as e:
        print(f"Error processing {raw_filename}: {e}")

def process_all_raw_images(input_folder):
    """
    Reads all .raw files from the input folder, computes their histograms, and saves them as .bin files.

    Parameters:
        input_folder (str): The directory containing the .raw files.
    """
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        return

    raw_files = [f for f in os.listdir(input_folder) if f.endswith(".raw")]
    
    if not raw_files:
        print("No .raw files found in the folder.")
        return

    for raw_file in raw_files:
        raw_path = os.path.join(input_folder, raw_file)
        bin_path = os.path.join(input_folder, raw_file.replace(".raw", ".bin"))

        compute_and_save_histogram(raw_path, bin_path)

if __name__ == "__main__":
    input_folder = os.path.join(os.getcwd(), "image_patterns")
    process_all_raw_images(input_folder)
