import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

KEY_STORE = "keys.json"

def _load_keys():
    """Load keys.json safely, reset if empty or corrupted."""
    if not os.path.exists(KEY_STORE):
        with open(KEY_STORE, "w") as f:
            json.dump({}, f)

    try:
        with open(KEY_STORE, "r") as f:
            data = f.read().strip()
            if not data:  # empty file
                return {}
            return json.loads(data)
    except (json.JSONDecodeError, ValueError):
        # If corrupted, reset to empty dict
        with open(KEY_STORE, "w") as f:
            json.dump({}, f)
        return {}

def _save_keys(keys):
    """Write keys dict back to file."""
    with open(KEY_STORE, "w") as f:
        json.dump(keys, f, indent=4)

def save_key(filename, key, nonce, tag):
    keys = _load_keys()
    keys[filename] = {
        "key": b64encode(key).decode(),
        "nonce": b64encode(nonce).decode(),
        "tag": b64encode(tag).decode()
    }
    _save_keys(keys)

def load_key(filename):
    keys = _load_keys()
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
