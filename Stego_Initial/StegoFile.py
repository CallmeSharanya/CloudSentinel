from PIL import Image

# Define the number of bits used to encode each character (8 bits for ASCII)
BITS_PER_CHAR = 8

def encode_file_in_rgb(image_path, file_path, output_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size

    # Read file as binary data
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Convert file data to binary string
    binary_file_data = ''.join([format(byte, '08b') for byte in file_data])
    binary_file_data += '0' * BITS_PER_CHAR  # Append null terminator

    # Encode binary file data into image's LSB
    encoded_pixels = []
    file_index = 0
    for pixel in pixels:
        if file_index < len(binary_file_data):
            r, g, b = pixel
            # Modify the LSB of each color channel (R, G, B) with the binary data
            r_bin = format(r, '08b')
            g_bin = format(g, '08b')
            b_bin = format(b, '08b')

            # Modify LSBs of RGB channels with binary file data bits
            r_bin = r_bin[:-1] + binary_file_data[file_index]
            g_bin = g_bin[:-1] + binary_file_data[file_index + 1] if file_index + 1 < len(binary_file_data) else g_bin
            b_bin = b_bin[:-1] + binary_file_data[file_index + 2] if file_index + 2 < len(binary_file_data) else b_bin

            # Append the modified pixel to the encoded list
            encoded_pixels.append((int(r_bin, 2), int(g_bin, 2), int(b_bin, 2)))
            file_index += 3  # Move forward 3 bits (one per channel)
        else:
            encoded_pixels.append(pixel)  # Add remaining pixels unchanged

    # Create the encoded image and save it
    encoded_img = Image.new("RGB", (width, height))
    encoded_img.putdata(encoded_pixels)
    encoded_img.save(output_path)
    print(f"File encoded and saved as RGB image at: {output_path}")

# Example usage
image_path = r"E:\Desktop\Stego.png" # Replace with your image path
file_path = r"E:\Desktop\CloudSentinel-main\PHEwith_xlsx\encrypted_ledger.json" # Replace with the path of the file you want to encode
output_path = r"E:\Desktop\EStegoFileDemo.png"

encode_file_in_rgb(image_path, file_path, output_path)
