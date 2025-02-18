import os
import numpy as np
import matplotlib.pyplot as plt

def read_raw_image(filepath, width=1920, height=1080):
    """
    Reads a raw image file that contains a 1920x1080 image stored as 16-bit unsigned integers.
    
    Parameters:
        filepath (str): Path to the raw file.
        width (int): Image width (default 1920).
        height (int): Image height (default 1080).
    
    Returns:
        image (np.ndarray): 2D array (height x width) of type uint16.
    """
    num_pixels = width * height
    expected_bytes = num_pixels * 2  # 2 bytes per pixel (16-bit)
    
    with open(filepath, "rb") as f:
        data = f.read()
    
    if len(data) != expected_bytes:
        raise ValueError(f"File {filepath} does not contain the expected number of bytes: expected {expected_bytes}, got {len(data)}")
    
    # Convert to numpy array of type uint16 and reshape to (height, width)
    image = np.frombuffer(data, dtype=np.uint16).reshape((height, width))
    return image

def compute_histogram(image):
    """
    Compute the histogram of a 10-bit image (values 0 to 1023).
    
    Parameters:
        image (np.ndarray): 2D image array.
        
    Returns:
        hist (np.ndarray): 1D histogram array with 1024 bins.
        bins (np.ndarray): Bin edges.
    """
    # Use bins from 0 to 1024 (which creates 1024 bins for values 0..1023)
    hist, bins = np.histogram(image, bins=np.arange(1025))
    return hist, bins

def main():
    # Directory containing raw files
    folder = "image_patterns"
    
    # List raw files (assumed extension .raw)
    raw_files = [f for f in os.listdir(folder) if f.lower().endswith(".raw")]
    
    if not raw_files:
        print("No raw files found in", folder)
        return

    for filename in raw_files:
        filepath = os.path.join(folder, filename)
        try:
            image = read_raw_image(filepath)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        hist, bins = compute_histogram(image)
        
        # Plot the histogram
        plt.figure(figsize=(10, 5))
        plt.bar(bins[:-1], hist, width=1, color="gray", edgecolor="black")
        plt.title(f"Histogram for {filename}")
        plt.xlabel("Pixel Value (0-1023)")
        plt.ylabel("Count")
        plt.xlim([0, 1023])
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
