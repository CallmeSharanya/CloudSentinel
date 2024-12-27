from PIL import Image

# Define the number of bits per character (8 bits per ASCII character)
BITS_PER_CHAR = 8

def decode_message_from_rgb(encoded_image_path):
    img = Image.open(encoded_image_path)
    pixels = list(img.getdata())
    
    binary_message = ""
    
    # Extract the LSB from each RGB channel for each pixel
    for pixel in pixels:
        r, g, b = pixel
        # Extract the LSB from each channel (R, G, B)
        binary_message += format(r, '08b')[-1]  # Last bit of R channel
        binary_message += format(g, '08b')[-1]  # Last bit of G channel
        binary_message += format(b, '08b')[-1]  # Last bit of B channel

    # Convert binary message into characters
    decoded_message = ""
    for i in range(0, len(binary_message), BITS_PER_CHAR):
        # Take chunks of BITS_PER_CHAR and convert them back to characters
        char_bin = binary_message[i:i + BITS_PER_CHAR]
        if len(char_bin) < BITS_PER_CHAR:
            break  # If the last chunk is less than 8 bits, we stop
        char = chr(int(char_bin, 2))  # Convert binary to ASCII
        if char == chr(0):  # Null character signifies the end of the message
            break
        decoded_message += char

    return decoded_message

# Example usage
encoded_image_path = r"D:\Desktop\Stego_rgb.png"  # Replace with your encoded image path

# Decode the message
decoded_message = decode_message_from_rgb(encoded_image_path)
print("Decoded message:", decoded_message)
