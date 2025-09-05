from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AES key (16 bytes = AES-128)
# In real-world apps, you'd use proper key management!
KEY = b"ThisIsASecretKey"  # must be exactly 16 bytes


def encrypt_file(input_file, output_file):
    """Encrypt a file with AES and save as binary format [nonce][tag][ciphertext]."""
    cipher = AES.new(KEY, AES.MODE_EAX)
    
    with open(input_file, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(output_file, "wb") as f:
        f.write(cipher.nonce)     # 16 bytes
        f.write(tag)              # 16 bytes
        f.write(ciphertext)       # rest of file


def decrypt_file(input_file, output_file):
    """Decrypt a file previously encrypted with AES."""
    with open(input_file, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    with open(output_file, "wb") as f:
        f.write(plaintext)


# Optional: run standalone for quick testing
if __name__ == "__main__":
    test_in = "plain.txt"
    test_enc = "encrypted.bin"
    test_dec = "decrypted.txt"

    # Write a sample file
    with open(test_in, "w") as f:
        f.write("Hello AES World!")

    # Encrypt
    encrypt_file(test_in, test_enc)
    print(f"Encrypted {test_in} -> {test_enc}")

    # Decrypt
    decrypt_file(test_enc, test_dec)
    print(f"Decrypted {test_enc} -> {test_dec}")
