#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define NUM_BINS      1024
#define NUM_CAMERAS   8
#define BYTES_PER_BIN 21   // 8 counts * 21 bits = 168 bits = 21 bytes per bin
#define TOTAL_BYTES   (NUM_BINS * BYTES_PER_BIN)

//---------------------------------------------------------------------------
// Function: pack_histograms
//
// Packs 8 histograms (each of 1024 bins) into the output_buffer.
//
// For each bin, the 8 counts (each 21 bits) are concatenated into a 168-bit
// value which is then stored in 21 bytes in little-endian order.
//---------------------------------------------------------------------------
void pack_histograms(uint32_t histograms[NUM_CAMERAS][NUM_BINS], uint8_t *output_buffer)
{
    for (size_t bin = 0; bin < NUM_BINS; bin++) {
        // Temporary container: 6 x 32-bit words = 192 bits (we only use 168 bits).
        uint32_t packed[6] = {0};
        int bit_pos = 0;  // current bit position within the 192-bit container

        // Pack each camera's count for this bin.
        for (size_t cam = 0; cam < NUM_CAMERAS; cam++) {
            uint32_t count = histograms[cam][bin];

            // Ensure the count fits in 21 bits.
            if (count >= (1UL << 21)) {
                fprintf(stderr, "Error: count %u at bin %zu in camera %zu exceeds 21 bits\n", count, bin, cam);
                exit(EXIT_FAILURE);
            }

            int word_index = bit_pos / 32;
            int bit_offset = bit_pos % 32;

            if (bit_offset <= 11) { // 32 - 21 = 11, so it fits in one word.
                packed[word_index] |= count << bit_offset;
            } else {
                // Count spans two 32-bit words.
                int bits_in_first = 32 - bit_offset;
                packed[word_index] |= count << bit_offset;           // lower part in current word
                packed[word_index + 1] |= count >> bits_in_first;      // upper part in next word
            }
            bit_pos += 21;
        }

        // Copy the lower 21 bytes (168 bits) into the output buffer in little-endian order.
        uint8_t *dest = output_buffer + (bin * BYTES_PER_BIN);
        uint8_t *src = (uint8_t *)packed;
        for (int i = 0; i < BYTES_PER_BIN; i++) {
            dest[i] = src[i];
        }
    }
}

//---------------------------------------------------------------------------
// Function: main
//
// Reads 8 histogram files from the directory "image_patterns", packs the
// histograms using pack_histograms(), and writes the output buffer to 
// "histograms_c.pack".
//---------------------------------------------------------------------------
int main(void)
{
    uint32_t histograms[NUM_CAMERAS][NUM_BINS];
    char filename[256];
    FILE *fp;

    // Read each of the 8 histogram files.
    for (int cam = 0; cam < NUM_CAMERAS; cam++) {
        // Construct the filename e.g. "image_patterns/pattern_1.bin"
        snprintf(filename, sizeof(filename), "image_patterns/pattern_%d.bin", cam + 1);
        fp = fopen(filename, "rb");
        if (fp == NULL) {
            fprintf(stderr, "Error: could not open file %s\n", filename);
            return EXIT_FAILURE;
        }
        // Read 1024 32-bit values for this camera.
        size_t items_read = fread(histograms[cam], sizeof(uint32_t), NUM_BINS, fp);
        if (items_read != NUM_BINS) {
            fprintf(stderr, "Error: file %s contains %zu bins instead of %d\n", filename, items_read, NUM_BINS);
            fclose(fp);
            return EXIT_FAILURE;
        }
        fclose(fp);
    }

    // Allocate the output buffer (21504 bytes).
    uint8_t *output_buffer = (uint8_t *)malloc(TOTAL_BYTES);
    if (output_buffer == NULL) {
        fprintf(stderr, "Error: could not allocate output buffer\n");
        return EXIT_FAILURE;
    }

    // Pack the histograms into the output buffer.
    pack_histograms(histograms, output_buffer);

    // Write the packed data to "histograms_c.pack".
    fp = fopen("histograms_c.pack", "wb");
    if (fp == NULL) {
        fprintf(stderr, "Error: could not open output file histograms_c.pack for writing\n");
        free(output_buffer);
        return EXIT_FAILURE;
    }
    size_t items_written = fwrite(output_buffer, 1, TOTAL_BYTES, fp);
    if (items_written != TOTAL_BYTES) {
        fprintf(stderr, "Error: only wrote %zu bytes (expected %d bytes)\n", items_written, TOTAL_BYTES);
        fclose(fp);
        free(output_buffer);
        return EXIT_FAILURE;
    }
    fclose(fp);

    free(output_buffer);
    printf("Successfully packed histograms into histograms_c.pack\n");

    return EXIT_SUCCESS;
}
