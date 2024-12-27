import sqlite3
import json
import pandas as pd
from phe import paillier
from PHEops import generate_keys, encrypt_balance, decrypt_balance, serialize_encrypted_balance


public_key, private_key = generate_keys()

def encrypt_table(db_path, table_name, column_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch data
    query = f'SELECT rowid, "{column_name}" FROM "{table_name}"'
    cursor.execute(query)
    rows = cursor.fetchall()

    encrypted_data = []
    for rowid, value in rows:
        if value is not None:
            encrypted_value = encrypt_balance(public_key, value)
            serialized_value = serialize_encrypted_balance(encrypted_value)
            encrypted_data.append({"rowid": rowid, "encrypted_value": serialized_value})
    
    conn.close()
    return encrypted_data

# Step 3: Update Encrypted Cell Value
def update_encrypted_cell(db_path, table_name, column_name, rowid, new_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Encrypt new value
    encrypted_new_value = encrypt_balance(public_key, new_value)
    serialized_value = serialize_encrypted_balance(encrypted_new_value)

    # Update cell
    query = f"""UPDATE "{table_name}"
                SET "{column_name}" = ?
                WHERE rowid = ?"""
    cursor.execute(query, [str(serialized_value), rowid])
    conn.commit()
    conn.close()

def export_encrypted_to_json(encrypted_data, json_path):
    with open(json_path, "w") as f:
        json.dump(encrypted_data, f)


db_path = 'bankexample.db'
table_name = 'Ledger'
column_name = "Bank Account Details - A/c No."  # Adjust to your actual column

encrypted_data = encrypt_table(db_path, table_name, column_name)
export_encrypted_to_json(encrypted_data, 'encrypted_ledger.json')


rowid_to_update = 4
new_balance = 51801504489  # Example new value
update_encrypted_cell(db_path, table_name, column_name, rowid_to_update, new_balance)
