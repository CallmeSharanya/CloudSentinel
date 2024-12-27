from phe import paillier
import json

# Load the public key
with open("public_key.json", "r") as pub_file:
    pub_data = json.load(pub_file)
    public_key = paillier.PaillierPublicKey(n=int(pub_data["n"]))

# Encrypt data
data = 12345  # Example data
encrypted_data = public_key.encrypt(data)
print(encrypted_data)

# Serialize encrypted data
encrypted_data_serialized = {
    "ciphertext": str(encrypted_data.ciphertext()),
    "exponent": encrypted_data.exponent
}

# Save encrypted data to a JSON file
with open("encrypted_data.json", "w") as enc_file:
    json.dump(encrypted_data_serialized, enc_file)

print("Data encrypted and saved locally.")
