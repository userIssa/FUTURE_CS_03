import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# AES settings
KEY_SIZE = 32  # AES-256
BLOCK_SIZE = AES.block_size

# Generate a static key (for demo); in production store securely
SECRET_KEY = base64.urlsafe_b64encode(get_random_bytes(KEY_SIZE))[:KEY_SIZE]

def encrypt_file(data: bytes) -> bytes:
    """Encrypt data using AES (CBC mode). Returns IV + ciphertext."""
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, BLOCK_SIZE))
    return cipher.iv + ct_bytes

def decrypt_file(enc_data: bytes) -> bytes:
    """Decrypt data using AES (CBC mode). Input must be IV + ciphertext."""
    iv = enc_data[:BLOCK_SIZE]
    ct = enc_data[BLOCK_SIZE:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt
