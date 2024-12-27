from phe import paillier


def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt_balance(public_key, balance):
    return public_key.encrypt(balance)

def decrypt_balance(private_key, encrypted_balance):
    return private_key.decrypt(encrypted_balance)

def serialize_encrypted_balance(encrypted_balance):
    return str(encrypted_balance.ciphertext()), encrypted_balance.exponent

def deserialize_encrypted_balance(public_key, serialized_balance):
    ciphertext, exponent = serialized_balance
    return paillier.EncryptedNumber(public_key, int(ciphertext), int(exponent))
