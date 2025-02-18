import os
import numpy as np

def read_fpga_histogram(filename):
    """
    Reads an FPGA histogram from a binary file.
    The file is expected to contain 1024 32-bit unsigned integers.
    """
    hist = np.fromfile(filename, dtype=np.uint32)
    if hist.size != 1024:
        raise ValueError(f"Unexpected histogram size in {filename}. Expected 1024, got {hist.size}")
    return hist

def pack_histograms(histograms, output_filename):
    """
    Packs 8 histograms into a single binary file.
    
    For each of the 1024 bins:
      - Pack the 8 counts (one per histogram) using 21 bits each.
      - The 8 counts are concatenated to form a 168-bit (21-byte) integer.
    
    The final file will be 21 bytes * 1024 = 21504 bytes.
    """
    num_bins = 1024
    num_images = len(histograms)
    
    packed_data = bytearray()
    
    for bin_idx in range(num_bins):
        packed_value = 0
        for img_idx in range(num_images):
            count = int(histograms[img_idx][bin_idx])
            # Ensure the count fits in 21 bits.
            if count >= (1 << 21):
                raise ValueError(f"Histogram count {count} at bin {bin_idx} in image {img_idx+1} exceeds 21 bits")
            # Pack: image1's count goes in bits 0-20, image2's in bits 21-41, etc.
            packed_value |= (count & ((1 << 21) - 1)) << (21 * img_idx)
        # Convert the 168-bit integer into 21 bytes (little-endian).
        packed_bytes = packed_value.to_bytes(21, byteorder='little')
        packed_data.extend(packed_bytes)
    
    with open(output_filename, "wb") as f:
        f.write(packed_data)
    
    print(f"Packed file saved to {output_filename}")

def main():
    input_folder = os.path.join(os.getcwd(), "image_patterns")
    
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")
    
    # Expect files named pattern_1.bin, pattern_2.bin, ..., pattern_8.bin
    pattern_files = sorted(
        [f for f in os.listdir(input_folder)
         if f.startswith("pattern_") and f.endswith(".bin")]
    )
    
    if len(pattern_files) != 8:
        raise ValueError(f"Expected 8 FPGA histogram files, but found {len(pattern_files)}")
    
    histograms = []
    for file in pattern_files:
        file_path = os.path.join(input_folder, file)
        print(f"Reading {file_path}...")
        hist = read_fpga_histogram(file_path)
        histograms.append(hist)
    
    output_filename = os.path.join(input_folder, "histograms.pack")
    pack_histograms(histograms, output_filename)

if __name__ == "__main__":
    main()
