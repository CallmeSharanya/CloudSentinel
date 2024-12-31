import pandas as pd
import json
import pandas as pd
from PHEops import *

def generate_keys_to_json():
    # generate keys
    public_key, private_key = generate_keys()
    # Save public key to a JSON file
    with open("public_key.json", "w") as pub_file:
        json.dump({"n": public_key.n}, pub_file)
    # Save the private key (store securely, do not share)
    with open("private_key.json", "w") as priv_file:
        json.dump({"p": private_key.p, "q": private_key.q}, priv_file)

    public_key_data = {"n": str(public_key.n)}
    with open("public_key.json", "w") as pub_file:
        json.dump(public_key_data, pub_file)

    # Save private key to a JSON file
    private_key_data = {
        "public_key": {"n": str(private_key.public_key.n)},
        "p": str(private_key.p),
        "q": str(private_key.q),
    }
    with open("private_key.json", "w") as priv_file:
        json.dump(private_key_data, priv_file)
    
    return public_key, private_key

def encrypt_file(public_key, filename): 
    # Load the public key
    with open("public_key.json", "r") as pub_file:
        pub_data = json.load(pub_file)
        public_key = paillier.PaillierPublicKey(n=int(pub_data["n"]))

    df = pd.read_excel(filename)

    df["Account ID_encr"] = df["Account ID"].apply(lambda acid: encrypt_string(public_key, acid))
    df["Phone Number_encr"] = df["Phone Number"].apply(lambda phno: encrypt_value(public_key, phno))
    df["Balance_encr"] = df["Balance"].apply(lambda balance: encrypt_value(public_key, balance))
    
    # Drop the plaintext balance column for security
    df = df.drop(columns=["Balance"])
    df = df.drop(columns=["Account ID"])
    df = df.drop(columns=["Phone Number"])

    # Save the encrypted DataFrame to a JSON file
    df.to_json("encrypted_BankLedger.json", orient="records")

    print("Excel sheet encrypted and saved as 'encrypted_BankLedger.json'.")

def decrypt_file(private_key, encrypted_filename, output_filename):
    """
    Decrypts an encrypted JSON file and saves the decrypted data to an Excel file.

    Parameters:
        private_key (paillier.PaillierPrivateKey): The private key for decryption.
        encrypted_filename (str): The path to the encrypted JSON file.
        output_filename (str): The path where the decrypted Excel file will be saved.
    """
    # Load the encrypted JSON file
    with open(encrypted_filename, "r") as enc_file:
        encrypted_data = json.load(enc_file)

    # Decrypt each column
    for record in encrypted_data:
        record["Account ID"] = decrypt_string(private_key, record["Account ID_encr"])
        record["Phone Number"] = decrypt_value(record["Phone Number_encr"])
        record["Balance"] = decrypt_value(record["Balance_encr"])

        # Remove encrypted columns for clarity
        del record["Account ID_encr"]
        del record["Phone Number_encr"]
        del record["Balance_encr"]

    # Convert decrypted data back to a DataFrame
    decrypted_df = pd.DataFrame(encrypted_data)

    # Save the decrypted data to an Excel file
    decrypted_df.to_excel(output_filename, index=False)

    print(f"Decrypted data saved to '{output_filename}'.")

public_key, private_key = generate_keys_to_json()
print("Keys generated and saved as 'public_key.json' and 'private_key.json'.")
encrypt_file(public_key, "./BankLedger.xlsx")
decrypt_file(private_key, "encrypted_BankLedger.json", "decrypted_BankLedger.xlsx")