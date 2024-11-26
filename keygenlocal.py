from phe import paillier
import json

# Generate Paillier key pair
public_key, private_key = paillier.generate_paillier_keypair()
print(public_key)
print(private_key)

# Save the public key
with open("public_key.json", "w") as pub_file:
    json.dump({"n": public_key.n}, pub_file)

# Save the private key (store securely, do not share)
with open("private_key.json", "w") as priv_file:
    json.dump({"p": private_key.p, "q": private_key.q}, priv_file)

print("Keys generated and saved locally.")
