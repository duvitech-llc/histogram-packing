import os
import numpy as np

def unpack_histograms(packed_filename, output_folder):
    """
    Unpacks a packed histogram file into 8 separate histogram files.
    
    The packed file is expected to be 21504 bytes long (1024 bins × 21 bytes per bin)
    where each 21-byte block contains eight 21-bit counts (one per histogram) stored
    consecutively (little-endian). This function extracts each 21-bit count and saves
    each histogram as a binary file with 1024 32-bit unsigned integers.
    
    Parameters:
        packed_filename (str): Path to the packed file (e.g., "histograms.pack").
        output_folder (str): Folder where the unpacked histogram files will be saved.
    """
    num_bins = 1024
    num_images = 8
    bin_size_bytes = 21
    expected_size = num_bins * bin_size_bytes

    # Read the entire packed file.
    with open(packed_filename, "rb") as f:
        data = f.read()
    
    if len(data) != expected_size:
        raise ValueError(f"Expected file size {expected_size} bytes, got {len(data)} bytes.")

    # Prepare 8 numpy arrays (one for each histogram) with 1024 bins each.
    histograms = [np.zeros(num_bins, dtype=np.uint32) for _ in range(num_images)]
    mask = (1 << 21) - 1  # Mask for 21 bits (0x1FFFFF)

    # Process each bin.
    for bin_idx in range(num_bins):
        offset = bin_idx * bin_size_bytes
        # Extract 21 bytes for the current bin.
        bin_bytes = data[offset:offset + bin_size_bytes]
        # Convert these 21 bytes (168 bits) into an integer (little-endian).
        bin_value = int.from_bytes(bin_bytes, byteorder='little')
        
        # For each histogram (0 to 7), extract the corresponding 21-bit segment.
        for img_idx in range(num_images):
            shift = img_idx * 21
            count = (bin_value >> shift) & mask
            histograms[img_idx][bin_idx] = count

    # Write each histogram out as a 32-bit binary file.
    for img_idx in range(num_images):
        output_filename = os.path.join(output_folder, f"pattern_unpacked_{img_idx+1}.bin")
        histograms[img_idx].tofile(output_filename)
        print(f"Saved unpacked histogram to {output_filename}")

def main():
    # Assume the packed file is in the 'image_patterns' directory.
    base_folder = os.path.join(os.getcwd(), "image_patterns")
    packed_file = os.path.join(base_folder, "histograms.pack")
    
    if not os.path.exists(packed_file):
        raise FileNotFoundError(f"Packed file not found: {packed_file}")
    
    unpack_histograms(packed_file, base_folder)

if __name__ == "__main__":
    main()
