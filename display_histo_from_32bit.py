import os
import numpy as np
import matplotlib.pyplot as plt

def load_histogram(bin_filename, num_bins=1024):
    """
    Reads a histogram from a .bin file.

    Parameters:
        bin_filename (str): Path to the histogram .bin file.
        num_bins (int): Number of bins in the histogram (1024 for 10-bit images).

    Returns:
        np.ndarray: Histogram values as an array.
    """
    try:
        with open(bin_filename, "rb") as f:
            histogram = np.frombuffer(f.read(), dtype=np.uint32)

        if histogram.size != num_bins:
            raise ValueError(f"Unexpected histogram size in {bin_filename}. Expected {num_bins}, got {histogram.size}")

        return histogram
    except Exception as e:
        print(f"Error reading {bin_filename}: {e}")
        return None

def display_histogram(bin_filename):
    """
    Loads and displays a histogram from a .bin file.

    Parameters:
        bin_filename (str): Path to the histogram .bin file.
    """
    histogram = load_histogram(bin_filename)
    if histogram is None:
        return

    # Plot histogram
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(histogram)), histogram, width=1.0, color='blue')
    plt.xlabel("Bin Index (0-1023)")
    plt.ylabel("Frequency")
    plt.title(f"Histogram from {os.path.basename(bin_filename)}")
    plt.grid(True)

    plt.show()

def main():
    input_folder = os.path.join(os.getcwd(), "image_patterns")
    
    # Find all .bin files
    bin_files = [f for f in os.listdir(input_folder) if f.endswith(".bin")]

    if not bin_files:
        print("No .bin files found in the folder.")
        return

    # Display histograms for all .bin files
    for bin_file in bin_files:
        bin_path = os.path.join(input_folder, bin_file)
        print(f"Displaying histogram: {bin_file}")
        display_histogram(bin_path)

if __name__ == "__main__":
    main()
