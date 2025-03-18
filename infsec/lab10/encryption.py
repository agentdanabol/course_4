from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad_pkcs7(data, block_size=16):
    padding_length = block_size - (len(data) % block_size)
    return data + bytes([padding_length] * padding_length)

def unpad_pkcs7(data):
    padding_length = data[-1]
    return data[:-padding_length]

def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

def encrypt_cbc(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad_pkcs7(plaintext)
    encrypted_blocks = []
    previous_block = iv
    
    for i in range(0, len(padded_text), 16):
        block = padded_text[i:i+16]
        block = xor_bytes(block, previous_block)
        encrypted_block = cipher.encrypt(block)
        encrypted_blocks.append(encrypted_block)
        previous_block = encrypted_block
    
    return iv + b''.join(encrypted_blocks)

def decrypt_cbc(key, ciphertext):
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_blocks = [ciphertext[i:i+16] for i in range(16, len(ciphertext), 16)]
    decrypted_blocks = []
    previous_block = iv
    
    for block in encrypted_blocks:
        decrypted_block = cipher.decrypt(block)
        decrypted_block = xor_bytes(decrypted_block, previous_block)
        decrypted_blocks.append(decrypted_block)
        previous_block = block
    
    return unpad_pkcs7(b''.join(decrypted_blocks))

def save_to_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def load_from_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

if __name__ == "__main__":
    key = get_random_bytes(32)  # 256-bit key
    iv = get_random_bytes(16)    # 16-byte IV
    plaintext = b"This is a secret message that needs encryption."
    
    encrypted = encrypt_cbc(key, iv, plaintext)
    save_to_file("infsec/lab10/encrypted.bin", encrypted)
    
    loaded_encrypted = load_from_file("infsec/lab10/encrypted.bin")
    decrypted = decrypt_cbc(key, loaded_encrypted)
    
    print("Original:", plaintext)
    print("Decrypted:", decrypted)
