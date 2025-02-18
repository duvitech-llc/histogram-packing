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
    # Directory containing the raw files
    folder = "image_patterns"
    # Get all files ending with .raw (case-insensitive)
    raw_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".raw")]
    raw_files.sort()  # Sort the file names (optional)
    
    if not raw_files:
        print("No raw files found in folder:", folder)
        return
    
    images = []
    hists = []   # List to store histograms
    bins_list = []  # List to store bins arrays
    
    # Read each raw file, compute its histogram, and store the data
    for file in raw_files:
        try:
            img = read_raw_image(file)
            h, b = compute_histogram(img)
            images.append(img)
            hists.append(h)
            bins_list.append(b)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    num_images = len(images)
    
    # Display the images in a 2x4 grid (or adjust the grid based on num_images)
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    for i in range(8):
        ax = axes[i]
        if i < num_images:
            # Scale 10-bit image (0-1023) to 8-bit (0-255) for display.
            img_disp = (images[i].astype(np.float32) * (255.0 / 1023.0)).astype(np.uint8)
            ax.imshow(img_disp, cmap="gray", vmin=0, vmax=255)
            ax.set_title(f"Image {i+1}")
        else:
            ax.axis("off")
        ax.axis("off")
    plt.tight_layout()
    plt.show()
    
    # Display the histograms in a 2x4 grid.
    fig2, axes2 = plt.subplots(2, 4, figsize=(16, 8))
    axes2 = axes2.flatten()
    for i in range(8):
        ax = axes2[i]
        if i < num_images:
            # Plot histogram: Use bins_list[i][:-1] for x values and hists[i] for counts.
            ax.bar(bins_list[i][:-1], hists[i], width=1, color="gray", edgecolor="black")
            ax.set_title(f"Histogram {i+1}")
            ax.set_xlabel("Pixel Value (0-1023)")
            ax.set_ylabel("Count")
            ax.set_xlim([0, 1023])
        else:
            ax.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
