from PIL import Image

# Define the number of bits per character (8 bits per byte)
BITS_PER_BYTE = 8

def decode_file_from_rgb(encoded_image_path, output_file_path):
    img = Image.open(encoded_image_path)
    pixels = list(img.getdata())
    
    binary_data = ""
    
    # Extract the LSB from each RGB channel for each pixel
    for pixel in pixels:
        r, g, b = pixel
        # Extract the LSB from each channel (R, G, B)
        binary_data += format(r, '08b')[-1]  # Last bit of R channel
        binary_data += format(g, '08b')[-1]  # Last bit of G channel
        binary_data += format(b, '08b')[-1]  # Last bit of B channel

    # Convert binary data into bytes
    file_bytes = bytearray()
    for i in range(0, len(binary_data), BITS_PER_BYTE):
        byte_bin = binary_data[i:i + BITS_PER_BYTE]
        if len(byte_bin) < BITS_PER_BYTE:
            break  # If the last chunk is less than 8 bits, we stop
        byte = int(byte_bin, 2)  # Convert binary to integer
        if byte == 0:  # Null byte signifies the end of the file
            break
        file_bytes.append(byte)

    # Write the decoded bytes to the output file
    with open(output_file_path, 'wb') as f:
        f.write(file_bytes)

    print(f"File decoded and saved at: {output_file_path}")

# Example usage
encoded_image_path = r"E:\Desktop\CloudSentinel-main\output_images\row_1.png" # Replace with your encoded image path
output_file_path = r"E:\Desktop\decoded_file1.txt"  # Replace with the path to save the decoded file

# Decode the file
decode_file_from_rgb(encoded_image_path, output_file_path)
