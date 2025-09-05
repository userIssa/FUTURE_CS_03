from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# Pad plaintext to be multiple of AES block size (16 bytes)
def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

# Encrypt file with AES
def encrypt_file(key, in_filename, out_filename):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(in_filename, 'rb') as f:
        plaintext = f.read()
    padded_plaintext = pad(plaintext)
    ciphertext = cipher.encrypt(padded_plaintext)

    with open(out_filename, 'wb') as f:
        # store the IV at the beginning so we can use it for decryption
        f.write(cipher.iv)
        f.write(ciphertext)

# Decrypt file with AES
def decrypt_file(key, in_filename, out_filename):
    with open(in_filename, 'rb') as f:
        iv = f.read(16)  # first 16 bytes = IV
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    # remove padding (trailing nulls)
    plaintext = plaintext.rstrip(b"\0")

    with open(out_filename, 'wb') as f:
        f.write(plaintext)


if __name__ == "__main__":
    key = get_random_bytes(32)  # AES-256 key (can be 16, 24, or 32 bytes)

    # Example usage
    encrypt_file(key, "plain.txt", "encrypted.bin")
    decrypt_file(key, "encrypted.bin", "decrypted.txt")

    print("✅ Encryption & Decryption complete")
