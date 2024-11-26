from phe import paillier
import json

# Load the public key
with open("public_key.json", "r") as pub_file:
    pub_data = json.load(pub_file)
    public_key = paillier.PaillierPublicKey(n=int(pub_data["n"]))

# Load the encrypted data
with open("encrypted_data.json", "r") as enc_file:
    encrypted_data_serialized = json.load(enc_file)

# Deserialize encrypted data
encrypted_data = paillier.EncryptedNumber(
    public_key,
    int(encrypted_data_serialized["ciphertext"]),
    int(encrypted_data_serialized["exponent"])
)

# Perform homomorphic addition
scalar_to_add = 1000  # Example scalar
encrypted_result = encrypted_data + scalar_to_add
print(encrypted_result)
# Serialize and save the result
result_serialized = {
    "ciphertext": str(encrypted_result.ciphertext()),
    "exponent": encrypted_result.exponent
}

with open("encrypted_result.json", "w") as result_file:
    json.dump(result_serialized, result_file)

print("Homomorphic addition performed. Result saved locally.")

