import os
import argparse

def extract_histogram(packed_filename, image_index):
    """
    Extracts the histogram for a specific image from the packed file.
    
    Parameters:
        packed_filename (str): Path to the packed file (expected 21504 bytes).
        image_index (int): Which histogram to extract (1 to 8, 1-indexed).
    
    Returns:
        list: A list of 1024 integer counts representing the histogram.
    """
    if image_index < 1 or image_index > 8:
        raise ValueError("Image index must be between 1 and 8.")
    
    num_bins = 1024
    segment_bits = 21           # each count is stored in 21 bits
    segment_mask = (1 << segment_bits) - 1  # mask to extract 21 bits (0x1FFFFF)
    bin_size_bytes = 21         # each bin is stored in 21 bytes
    expected_size = bin_size_bytes * num_bins  # should be 21504 bytes

    # Read the entire packed file
    with open(packed_filename, "rb") as f:
        data = f.read()
    
    if len(data) != expected_size:
        raise ValueError(f"Unexpected file size: expected {expected_size} bytes, got {len(data)} bytes")
    
    histogram = []
    for bin_idx in range(num_bins):
        start = bin_idx * bin_size_bytes
        end = start + bin_size_bytes
        bin_bytes = data[start:end]
        # Convert the 21 bytes (168 bits) into an integer (little-endian)
        bin_value = int.from_bytes(bin_bytes, byteorder='little')
        # Each histogram's count is stored in a consecutive 21-bit field.
        # For image_index (1-indexed), the bits are at offset (image_index-1)*21.
        shift = (image_index - 1) * segment_bits
        count = (bin_value >> shift) & segment_mask
        histogram.append(count)
    
    return histogram

def main():
    parser = argparse.ArgumentParser(
        description="Extract and display a histogram from a packed file."
    )
    parser.add_argument(
        "index",
        type=int,
        help="Histogram index to extract (1-8)"
    )
    parser.add_argument(
        "--file",
        type=str,
        default="histograms.pack",
        help="Path to the packed histogram file (default: histograms.pack)"
    )
    args = parser.parse_args()

    try:
        hist = extract_histogram(args.file, args.index)
    except Exception as e:
        print("Error:", e)
        return

    # Display a preview of the histogram (first 20 bins)
    print(f"Extracted histogram for pattern {args.index}:")
    print(hist[:20], "...")
    
    # Optionally, plot the histogram if matplotlib is available
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.bar(range(len(hist)), hist, width=1, color='blue')
        plt.title(f"Histogram for Pattern {args.index}")
        plt.xlabel("Bin")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("matplotlib is not installed; skipping plot.")

if __name__ == "__main__":
    main()
