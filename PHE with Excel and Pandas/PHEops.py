from phe import paillier

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt_value(public_key, value):
    encrypted_value =  public_key.encrypt(value)
    return {
        "ciphertext": str(encrypted_value.ciphertext()),
        "exponent": encrypted_value.exponent
    }

def decrypt_value(private_key, encrypted_value):
    ciphertext = int(encrypted_value["ciphertext"])
    exponent = encrypted_value["exponent"]
    encrypted_number = paillier.EncryptedNumber(private_key.public_key, ciphertext, exponent)
    return private_key.decrypt(encrypted_number)

def encrypt_string(public_key, text):
    # Convert the string to a numerical representation
    text_as_int = int.from_bytes(text.encode('utf-8'), byteorder='big')
    # Encrypt the number
    encrypted_value = public_key.encrypt(text_as_int)
    return {
        "ciphertext": str(encrypted_value.ciphertext()),
        "exponent": encrypted_value.exponent
    }

def decrypt_string(private_key, encrypted_value):
    """
    Decrypts an encrypted string value.

    Parameters:
        private_key (paillier.PaillierPrivateKey): The private key for decryption.
        encrypted_value (dict): A dictionary containing the encrypted value as "ciphertext" (string) and "exponent" (integer).

    Returns:
        str: The decrypted string.
    """
    # Extract ciphertext and exponent from the encrypted_value dictionary
    ciphertext = int(encrypted_value["ciphertext"])
    exponent = encrypted_value["exponent"]

    # Reconstruct the EncryptedNumber object
    encrypted_number = paillier.EncryptedNumber(private_key.public_key, ciphertext, exponent)

    # Decrypt the integer representation
    decrypted_number = private_key.decrypt(encrypted_number)

    # Convert the decrypted number back to a string
    decrypted_text = decrypted_number.to_bytes((decrypted_number.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
    return decrypted_text

# def serialize_encrypted_value(encrypted_value):
#     return str(encrypted_value.ciphertext()), encrypted_value.exponent

# def deserialize_encrypted_value(public_key, serialized_value):
#     ciphertext, exponent = serialized_value
#     return paillier.EncryptedNumber(public_key, int(ciphertext), int(exponent))



# public_key, private_key = generate_keys()
# encrypted = encrypt_string(public_key, "Hello World")
# # serialised = serialize_encrypted_value(encrypted)
# print(encrypted)
# print(decrypt_string(private_key, encrypted))
