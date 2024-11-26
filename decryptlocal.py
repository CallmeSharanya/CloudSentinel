from phe import paillier
import json

with open("public_key.json", "r") as pub_file:
    pub_data = json.load(pub_file)
    public_key = paillier.PaillierPublicKey(n=int(pub_data["n"]))
# Load the private key
with open("private_key.json", "r") as priv_file:
    priv_data = json.load(priv_file)
    private_key = paillier.PaillierPrivateKey(
        p=int(priv_data["p"]),
        q=int(priv_data["q"]),
        public_key=public_key 
    )

'''# Load the public key (needed to initialize encrypted number objects)
with open("public_key.json", "r") as pub_file:
    pub_data = json.load(pub_file)
    public_key = paillier.PaillierPublicKey(n=int(pub_data["n"]))
private_key.public_key=public_key'''    

# Load the encrypted result
with open("encrypted_result.json", "r") as result_file:
    result_serialized = json.load(result_file)

# Deserialize encrypted result
encrypted_result = paillier.EncryptedNumber(
    public_key,
    int(result_serialized["ciphertext"]),
    int(result_serialized["exponent"])
)

# Decrypt the result
decrypted_result = private_key.decrypt(encrypted_result)

print("Decrypted result:", decrypted_result)
