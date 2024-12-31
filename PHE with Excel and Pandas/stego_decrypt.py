import os
import json
from PIL import Image
from typing import Dict, Any


class ImageSteganography:
    END_MARKER = '11111111'
    FIELD_SEPARATOR = '11110000'

    def binary_to_int(self, binary: str) -> int:
        """Convert binary string to integer"""
        return int(binary, 2)

    def decode_data_from_image(self, image_path: str) -> Dict[str, Any]:
        """Extract and decode data from an image"""
        # Load image and convert it to RGB 
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        pixels = list(img.getdata())
    
        # Extract binary data from LSBs
        binary_data = ''
        for r, g, b in pixels:
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
    
        # Find the end marker and discard everything after and including it
        end_idx = binary_data.find(self.END_MARKER)
        if end_idx == -1:
            raise ValueError("End marker not found in the image.")
        binary_data = binary_data[:end_idx-1]  # Keep everything before the marker
    
        # Split binary data into parts using the FIELD_SEPARATOR
        parts = binary_data.split(self.FIELD_SEPARATOR)
    
        # Decode the parts
        decoded_data = {}
    
        # Process each part by grouping binary data into 8-bit chunks and converting to integers
        field_labels = ['Account ID_encr', 'Phone Number_encr', 'Balance_encr']  # Specify the field labels for the parts
        for i, part in enumerate(parts):
            if i >= len(field_labels):  # Prevent out-of-index errors if more parts than labels
                break
            
            decoded_integers = []
    
            for j in range(0, len(part), 8):
                byte = part[j:j + 8]
                if len(byte) < 8:
                    byte = byte.ljust(8, '0')  # Pad incomplete byte with zeros
    
                try:
                    decoded_integers.append(self.binary_to_int(byte))  # Convert to integer
                except ValueError as e:
                    print(f"Error decoding byte: {byte}, {e}")
                    continue
                
            # Add the decoded integers as a concatenated string to the dictionary
            decoded_data[field_labels[i]] = ''.join(map(str, decoded_integers))
    
        return decoded_data



def decrypt_stego_image(image_path: str, output_json_path: str):
    stego = ImageSteganography()

    # Decode the image to extract the binary data
    decoded_data = stego.decode_data_from_image(image_path)

    # Save decoded data to json
    with open(output_json_path, 'w') as f:
        json.dump(decoded_data, f, indent=4)

    print(f"Decoded data saved to {output_json_path}")


if __name__ == "__main__":
    # Decode this particular user
    image_path = r"encoded_img\image_ratna.png"  # Path to encoded image: change this acc. to the required user
    output_json_path = r"decrypted_rows\decoded_ratna.json"  # Path to save the decoded json: change the name of the file acc. to the user

    decrypt_stego_image(image_path, output_json_path)
