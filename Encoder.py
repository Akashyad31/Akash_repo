# encoder.py

import json
import hashlib
import numpy as np
from datetime import datetime, date

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return int(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert NumPy arrays to Python lists
        return super(NumpyEncoder, self).default(obj)

def convert_to_chars(input_string):
    # Convert each character to its ASCII code and concatenate
    return ''.join(str(ord(char)) for char in input_string)

def encrypt_header(oct_vol):
    # Convert np.int32 and np.uint64 values to Python integers, and np.ndarray to Python lists in the header
    converted_header = {key: int(value) if isinstance(value, (np.int32, np.uint64)) else value.tolist() if isinstance(value, np.ndarray) else value for key, value in oct_vol.header.items()}

    # Extract required fields
    id_value = oct_vol.header['id']
    patient_id_value = oct_vol.header['patient_id']
    dob_value = str(oct_vol.header['dob'])

    # Encrypt each value using SHA-3 (SHA-3-256 in this case) and convert to characters
    encrypted_id = convert_to_chars(hashlib.sha3_256(id_value.encode()).hexdigest())
    encrypted_patient_id = convert_to_chars(hashlib.sha3_256(patient_id_value.encode()).hexdigest())
    encrypted_dob = convert_to_chars(hashlib.sha3_256(dob_value.encode()).hexdigest())

    # Create a copy of the header to avoid modifying the original header
    encrypted_header = converted_header.copy()

    # Update the encrypted fields in the copied header
    encrypted_header['id'] = encrypted_id
    encrypted_header['patient_id'] = encrypted_patient_id
    encrypted_header['dob'] = encrypted_dob

    # Create a dictionary with the entire header (with specific fields encrypted)
    result_dict = {
        'header': encrypted_header
    }

    return result_dict

def save_encrypted_header(oct_vol, output_json_path):
    # Encrypt the header
    encrypted_data = encrypt_header(oct_vol)

    # Convert the dictionary to JSON using the custom encoder and store it in a file
    with open(output_json_path, 'w') as json_file:
        json.dump(encrypted_data, json_file, indent=2, cls=NumpyEncoder)  # Adding indent for better readability

    # Print the path to the generated JSON file
    print(f"Encrypted header data stored in: {output_json_path}")
