import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_test_pattern(pattern_index, height=1080, width=1920):
    """
    Generate one of eight 10-bit test pattern images.
    The pixel values are in the range 0 to 1023 (10-bit).
    
    Pattern choices:
      1. Horizontal gradient
      2. Vertical gradient
      3. Diagonal gradient
      4. Monochrome Bars
      5. Radial gradient from center
      6. Horizontal sine wave
      7. Random noise
      8. Constant mid-level (512)
      
    Returns:
        image (np.ndarray): A (height x width) uint16 array with values 0–1023.
    """
    if pattern_index == 1:
        # Horizontal gradient: left=0, right=1023
        row = np.linspace(0, 1023, width, dtype=np.uint16)
        image = np.tile(row, (height, 1))
    elif pattern_index == 2:
        # Vertical gradient: top=0, bottom=1023
        col = np.linspace(0, 1023, height, dtype=np.uint16)
        image = np.repeat(col[:, np.newaxis], width, axis=1)
    elif pattern_index == 3:
        # Diagonal gradient: combination of horizontal and vertical
        x = np.linspace(0, width-1, width, dtype=np.float32)
        y = np.linspace(0, height-1, height, dtype=np.float32)
        xv, yv = np.meshgrid(x, y)
        image = ((xv + yv) / ((width-1) + (height-1)) * 1023).astype(np.uint16)
    elif pattern_index == 4:
        # Generate 10 monochrome bars across the width of the image
        num_bars = 10
        bar_width = width // num_bars
        bar_values = np.linspace(0, 1023, num_bars, dtype=np.uint16)

        image = np.zeros((height, width), dtype=np.uint16)
        for i in range(num_bars):
            image[:, i * bar_width:(i + 1) * bar_width] = bar_values[i]

        # Ensure the last bar covers any remaining pixels due to rounding
        image[:, num_bars * bar_width:] = bar_values[-1]
    elif pattern_index == 5:
        # Radial gradient: distance from center normalized to 0-1023.
        y = np.linspace(0, height-1, height)
        x = np.linspace(0, width-1, width)
        xv, yv = np.meshgrid(x, y)
        cx, cy = (width-1)/2, (height-1)/2
        dist = np.sqrt((xv - cx)**2 + (yv - cy)**2)
        max_dist = np.sqrt(cx**2 + cy**2)
        image = (dist / max_dist * 1023).astype(np.uint16)
    elif pattern_index == 6:
        # Horizontal sine wave.
        x = np.linspace(0, 2*np.pi, width, dtype=np.float32)
        sine_row = ((np.sin(x) + 1) / 2 * 1023).astype(np.uint16)
        image = np.tile(sine_row, (height, 1))
    elif pattern_index == 7:
        # Random noise.
        image = np.random.randint(0, 1024, size=(height, width), dtype=np.uint16)
    elif pattern_index == 8:
        # Constant mid-level.
        image = np.full((height, width), 512, dtype=np.uint16)
    else:
        raise ValueError("Invalid pattern index")
    
    return image

def save_raw16(image, filename):
    """
    Save a 16-bit image as a raw binary file.
    Each pixel is stored as a 16-bit unsigned integer in native byte order.
    
    Parameters:
        image (np.ndarray): A uint16 image array.
        filename (str): The destination filename.
    """
    # Write the raw binary data (each pixel 2 bytes)
    with open(filename, "wb") as f:
        f.write(image.tobytes())

def main():
    # Create the output folder "image_patterns"
    output_folder = os.path.join(os.getcwd(), "image_patterns")
    os.makedirs(output_folder, exist_ok=True)
    
    patterns = []
    
    # Generate 8 patterns
    for i in range(1, 9):
        img = generate_test_pattern(i, height=1080, width=1920)
        patterns.append(img)
        
        # Save as raw file (each pixel is stored as a 16-bit integer)
        raw_filename = os.path.join(output_folder, f"pattern_{i}.raw")
        save_raw16(img, raw_filename)
        print(f"Saved RAW: {raw_filename}")
    
    # Display the 8 generated images in a 2x4 grid.
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for idx, img in enumerate(patterns):
        ax = axes[idx//4, idx%4]
        # For display, we can scale the 10-bit image (0-1023) to 8-bit (0-255)
        display_img = (img.astype(np.float32) * (255.0 / 1023.0)).astype(np.uint8)
        ax.imshow(display_img, cmap='gray', vmin=0, vmax=255)
        ax.set_title(f"Pattern {idx+1}")
        ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
