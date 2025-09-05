import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

KEY_STORE = "keys.json"

# Ensure keys.json exists and is not empty
if not os.path.exists(KEY_STORE) or os.path.getsize(KEY_STORE) == 0:
    with open(KEY_STORE, "w") as f:
        json.dump({}, f)

def save_key(filename, key, nonce, tag):
    with open(KEY_STORE, "r+") as f:
        keys = json.load(f)
        keys[filename] = {
            "key": b64encode(key).decode(),
            "nonce": b64encode(nonce).decode(),
            "tag": b64encode(tag).decode()
        }
        f.seek(0)
        json.dump(keys, f, indent=4)
        f.truncate()

def load_key(filename):
    with open(KEY_STORE, "r") as f:
        keys = json.load(f)
        return {
            "key": b64decode(keys[filename]["key"]),
            "nonce": b64decode(keys[filename]["nonce"]),
            "tag": b64decode(keys[filename]["tag"])
        }

def encrypt_file(file_data, filename):
    key = get_random_bytes(32)  # AES-256
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)

    save_key(filename, key, cipher.nonce, tag)
    return ciphertext

def decrypt_file(ciphertext, filename):
    data = load_key(filename)
    cipher = AES.new(data["key"], AES.MODE_EAX, nonce=data["nonce"])
    plaintext = cipher.decrypt_and_verify(ciphertext, data["tag"])
    return plaintext
