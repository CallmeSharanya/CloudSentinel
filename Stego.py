from PIL import Image

# Define the number of bits used to encode each character (8 bits for ASCII)
BITS_PER_CHAR = 8

def encode_message_in_rgb(image_path, message, output_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size

    # Convert message to binary string
    message += chr(0)  # Append null character to signify end of message
    binary_message = ''.join([format(ord(char), f'0{BITS_PER_CHAR}b') for char in message])

    # Encode message into image's LSB
    encoded_pixels = []
    message_index = 0
    for pixel in pixels:
        if message_index < len(binary_message):
            r, g, b = pixel
            # Modify the LSB of each color channel (R, G, B) with the message's binary bits
            r_bin = format(r, '08b')
            g_bin = format(g, '08b')
            b_bin = format(b, '08b')

            # Modify LSBs of RGB channels with binary message bits
            r_bin = r_bin[:-1] + binary_message[message_index]
            g_bin = g_bin[:-1] + binary_message[message_index + 1] if message_index + 1 < len(binary_message) else g_bin
            b_bin = b_bin[:-1] + binary_message[message_index + 2] if message_index + 2 < len(binary_message) else b_bin

            # Append the modified pixel to the encoded list
            encoded_pixels.append((int(r_bin, 2), int(g_bin, 2), int(b_bin, 2)))
            message_index += 3  # Move forward 3 bits (one per channel)
        else:
            encoded_pixels.append(pixel)  # Add remaining pixels unchanged

    # Create the encoded image and save it
    encoded_img = Image.new("RGB", (width, height))
    encoded_img.putdata(encoded_pixels)
    encoded_img.save(output_path)
    print(f"Message encoded and saved as RGB image at: {output_path}")

# Example usage
image_path = r"D:\Desktop\StegoDemo.png"  # Replace with your image path
output_path = r"D:\Desktop\Stego_rgb.png"
message = "12345"

encode_message_in_rgb(image_path, message, output_path)
