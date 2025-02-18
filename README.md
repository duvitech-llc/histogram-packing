# Histogram Packing

This repository contains a C implementation for efficiently packing and unpacking histogram data from eight camera sensors. Each sensor provides a histogram with 1024 bins, where each bin count is a 21-bit integer. The packing process concatenates eight 21-bit counts (one per sensor) into a single 168-bit (21-byte) block per bin. The final packed file is exactly 21504 bytes (1024 bins × 21 bytes).

This project is optimized for the STM32H7 MCU but can also be built and run on a PC for testing and development.

## Features

- **Efficient Packing:** Pack 8 histograms (1024 bins each) into a compact binary format.
- **Unpacking Function:** Retrieve the original histogram data from the packed binary.
- **File I/O Example:** A `main.c` demonstrating how to:
  - Read histogram data from 8 binary files (`pattern_1.bin` to `pattern_8.bin`) located in the `image_patterns` directory.
  - Pack the histograms using the provided packing function.
  - Write the output buffer to a binary file (`histograms_c.pack`).
- **Cross-Platform:** While optimized for STM32H7, the code builds with standard GCC (or your chosen cross-compiler).

## Repository Structure
```
histogram-packing/ 
├── image_patterns/ # Directory for test images and histogram binary files (pattern_1.bin to pattern_8.bin)
├── .gitignore # Git ignore rules
├── Makefile # Build instructions for compiling the project
├── binary_compare.py # Compare histograms to packed histograms
├── display_histo_from_32bit.py # Display histograms with 32bit bins
├── display_histograms.py # Display histograms from raw image data
├── display_patterns_and_histograms.py # Display test patterns and their histograms
├── export_32bit_histogram.py # Export 32bit bin histogram from raw test patterns
├── export_histogram2text.py # Export csv histogram bin, value for raw test patterns
├── generate_test_patterns.py # Generate 10-bit monochrome raw test patterns
├── main.c # Main program demonstrating read/pack/write includes implementation of pack and unpack histograms functions
├── pack_histograms.py # Packs 8 histograms into one file
├── unpack_histograms.py # Unpacks 8 histograms from one file
├── view_histogram_from_packed.py # View histograms from packed file
└── README.md # This file

```

> **Note:** Adjust the file names and structure as needed if your repository layout differs.

## Python Instructions

## Build Instructions for C

1. **Generate Test Patterns:**
   ```bash
   python generate_test_patterns.py
   python display_patterns_and_histograms.py
   ```

2. **Export 32bit histograms:**
   ```bash
   python export_32bit_histogram.py
   ```

3. **Pack histograms:**
   ```bash
   python pack_histograms.py
   python view_histogram_from_packed.py
   ```
   
3. **Unpack histograms:**
   ```bash
   python unpack_histograms.py
   python binary_compare.py 
   ```

### For PC (GCC)
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/duvitech-llc/histogram-packing.git
   cd histogram-packing
   ```

2. **Build the Executable:**
   ```bash
   make
   ```

3. **Clean Build Artifacts:**
   ```bash
   make clean
   ```

4. **Binary compare packed files:**
   ```bash
   cmp histograms_c.pack image_patterns/histograms.pack 
   ```
