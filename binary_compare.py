import os

def binary_compare(file1, file2):
    """
    Compare two binary files byte-by-byte.

    Parameters:
        file1 (str): Path to the first binary file.
        file2 (str): Path to the second binary file.

    Returns:
        bool: True if files are identical, False otherwise.
    """
    try:
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            data1 = f1.read()
            data2 = f2.read()

            if data1 == data2:
                return True
            else:
                # Find first difference index
                min_length = min(len(data1), len(data2))
                for i in range(min_length):
                    if data1[i] != data2[i]:
                        print(f"Mismatch at byte {i}: {data1[i]} != {data2[i]}")
                        break
                
                print(f"Files differ in size or content: {file1} vs {file2}")
                return False
    except FileNotFoundError:
        print(f"Error: One of the files {file1} or {file2} not found!")
        return False

def compare_all_histograms(input_folder, num_patterns=8):
    """
    Compare all pattern_{i}.bin files to unpacked_pattern_{i}.bin files.

    Parameters:
        input_folder (str): Folder where the files are located.
        num_patterns (int): Number of patterns to compare.
    """
    all_match = True

    for i in range(1, num_patterns + 1):
        original_file = os.path.join(input_folder, f"pattern_{i}.bin")
        unpacked_file = os.path.join(input_folder, f"pattern_unpacked_{i}.bin")

        if os.path.exists(original_file) and os.path.exists(unpacked_file):
            if binary_compare(original_file, unpacked_file):
                print(f"✅ Files match: {original_file} == {unpacked_file}")
            else:
                print(f"❌ Mismatch: {original_file} != {unpacked_file}")
                all_match = False
        else:
            print(f"⚠️ Missing file: {original_file} or {unpacked_file}")
            all_match = False

    if all_match:
        print("\n🎉 All files match perfectly!")
    else:
        print("\n❗ Some files have mismatches!")

def main():
    input_folder = os.path.join(os.getcwd(), "image_patterns")
    
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        return

    compare_all_histograms(input_folder)

if __name__ == "__main__":
    main()
