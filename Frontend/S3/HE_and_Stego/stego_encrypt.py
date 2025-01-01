import json
import os
import random
from PIL import Image

BITS_PER_CHAR = 8
END_MARKER = '11111111'  # Unique pattern to mark the end of the encoded data
FIELD_SEPARATOR = '11110000'  # Unique pattern to separate fields

def encode_file_in_rgb(image_path, data, output_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size

    file_index = 0
    encoded_pixels = []

    # Encode binary data into image pixels (modifying LSBs)
    for pixel in pixels:
        if file_index < len(data):
            if len(pixel) == 3:
                r, g, b = pixel  # RGB image
            #elif len(pixel) == 4:
               # r, g, b, a = pixel  # RGBA image (ignore alpha for encoding)
            else:
                encoded_pixels.append(pixel)  # Skip unexpected pixel formats
                continue

            r_bin = format(r, '08b')
            g_bin = format(g, '08b')
            b_bin = format(b, '08b')

            # Modify the LSBs of the RGB channels with binary file data bits
            r_bin = r_bin[:-1] + data[file_index] if file_index < len(data) else r_bin
            file_index += 1
            g_bin = g_bin[:-1] + data[file_index] if file_index < len(data) else g_bin
            file_index += 1
            b_bin = b_bin[:-1] + data[file_index] if file_index < len(data) else b_bin
            file_index += 1

            # Append the modified pixel to the encoded list
            if len(pixel) == 3:
                encoded_pixels.append((int(r_bin, 2), int(g_bin, 2), int(b_bin, 2)))
            #else:
                #encoded_pixels.append((int(r_bin, 2), int(g_bin, 2), int(b_bin, 2), a))  # Keep the alpha channel as is
        else:
            encoded_pixels.append(pixel)  # Add remaining pixels unchanged

    # Ensure the image is large enough for the data
    if file_index < len(data):
        raise ValueError("Image is too small to hold the encoded data.")

    # Create the encoded image and save it
    encoded_img = Image.new("RGBA" if len(pixels[0]) == 4 else "RGB", (width, height))
    encoded_img.putdata(encoded_pixels)
    encoded_img.save(output_path)
    print(f"Data encoded and saved as RGB image at: {output_path}")


def encode_json_rows_into_images(json_data, images_directory, output_directory):    
    if not isinstance(json_data, list):
        raise ValueError("JSON data must be a list of rows.")

    # Get all images from the images directory
    image_files = [os.path.join(images_directory, img) for img in os.listdir(images_directory) if img.endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        raise ValueError("No images found in the images directory.")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through JSON rows and encode all fields into a single image
    i = 0
    encoded_image_path = []
    for row in json_data:
        name = row.get("Name")
        if name is None:
            print(f"Skipping row without a 'Name': {row}")
            continue

        # Combine all ciphertext fields into a single binary data string
        combined_data = ''
        for field_name, field_value in row.items():
            if isinstance(field_value, dict) and "ciphertext" in field_value:  # Check if the key corresponds to a ciphertext field
                field_data = field_value["ciphertext"]  # Extract ciphertext value
                
                # Process each character in the ciphertext
                for char in field_data:
                    if char.isdigit():  # Ensure the character is numeric
                        char_binary = format(int(char), '08b')  # Convert to 8-bit binary
                        combined_data += char_binary  # Append binary representation
                combined_data += FIELD_SEPARATOR  # Add field separator after each field

        # Remove trailing separator
        last_occurrence_index = combined_data.rfind(FIELD_SEPARATOR)
        if last_occurrence_index != -1:
            combined_data = combined_data[:last_occurrence_index] + combined_data[last_occurrence_index + len(FIELD_SEPARATOR)-1:]
        combined_data += END_MARKER  # Add end marker

        # Select a random image
        image_path = random.choice(image_files)
        output_path = os.path.join(output_directory, f"image_{name.lower()}.png")

        # Encode the combined data into the image
        encode_file_in_rgb(image_path, combined_data, output_path)

        print(f"{name} encoded in {output_path}")
        encoded_image_path.append(output_path)
    print(encoded_image_path)
    return encoded_image_path

if __name__ == "__main__":
    # Example usage
    json_file = r"encrypted_BankLedger.json"  # Path to the JSON file
    images_directory = r"images"  # Path to the directory containing images
    output_directory = r"encoded_img"  # Directory to save output images

    encode_json_rows_into_images(json_file, images_directory, output_directory)