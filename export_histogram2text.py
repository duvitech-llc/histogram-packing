import os
import numpy as np

def read_raw_image(filepath, width=1920, height=1080):
    """
    Reads a raw image file that contains a 1920x1080 image stored as 16-bit unsigned integers.
    
    Parameters:
        filepath (str): Path to the raw file.
        width (int): Image width (default 1920).
        height (int): Image height (default 1080).
    
    Returns:
        np.ndarray: 2D array (height x width) of type uint16.
    """
    num_pixels = width * height
    expected_bytes = num_pixels * 2  # 2 bytes per pixel (16-bit)
    
    with open(filepath, "rb") as f:
        data = f.read()
    
    if len(data) != expected_bytes:
        raise ValueError(f"File {filepath} does not contain the expected number of bytes: expected {expected_bytes}, got {len(data)}")
    
    image = np.frombuffer(data, dtype=np.uint16).reshape((height, width))
    return image

def compute_histogram(image):
    """
    Compute the histogram of a 10-bit image (values 0 to 1023).
    
    Parameters:
        image (np.ndarray): 2D image array.
        
    Returns:
        hist (np.ndarray): 1D histogram array with 1024 bins.
    """
    # Create bins from 0 to 1024 to get 1024 bins for pixel values 0...1023.
    hist, _ = np.histogram(image, bins=np.arange(1025))
    return hist

def save_histogram_to_text(hist, output_filename):
    """
    Save the histogram as a comma-delimited text file with two columns: bin, count.
    
    Parameters:
        hist (np.ndarray): 1D histogram array.
        output_filename (str): Path to the output text file.
    """
    with open(output_filename, "w") as f:
        for bin_val, count in enumerate(hist):
            f.write(f"{bin_val},{count}\n")

def main():
    # Folder containing the raw files
    folder = "image_patterns"
    # List all .raw files (case-insensitive)
    raw_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".raw")]
    raw_files.sort()  # Optional sorting

    if not raw_files:
        print("No raw files found in folder:", folder)
        return

    for raw_file in raw_files:
        try:
            image = read_raw_image(raw_file)
        except Exception as e:
            print(f"Error reading {raw_file}: {e}")
            continue
        
        hist = compute_histogram(image)
        # Construct output filename: same base name, with extension .txt (or .csv)
        base_name = os.path.splitext(os.path.basename(raw_file))[0]
        output_filename = os.path.join(folder, f"{base_name}_hist.txt")
        save_histogram_to_text(hist, output_filename)
        print(f"Saved histogram for {raw_file} to {output_filename}")

if __name__ == "__main__":
    main()
