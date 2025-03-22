import os
import random

POLYNOMIAL = 0x187  # x^8 + x^7 + x^2 + x + 1

BLOCK_SIZE = 4

def generate_s_blocks():
    pi0 = list(range(256))
    random.shuffle(pi0)
    pi1 = list(range(256))
    random.shuffle(pi1)
    return pi0, pi1

def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def gf_multiply(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= POLYNOMIAL
        b >>= 1
    return result

def R(block):
    return bytes([block[-1]]) + block[:-1]

def L(block):
    for _ in range(BLOCK_SIZE):
        block = R(block)
        block = xor_bytes(block, bytes([gf_multiply(block[0], 0x1B)]))
    return block

def L_inv(block):
    for _ in range(BLOCK_SIZE):
        block = xor_bytes(block, bytes([gf_multiply(block[0], 0x1B)]))
        block = block[1:] + bytes([block[0]])
    return block

def generate_round_keys(key):
    keys = [key[:BLOCK_SIZE], key[BLOCK_SIZE:]]
    for i in range(2, 10):
        keys.append(L(keys[i-1]))
    return keys

def encrypt_block(block, keys):
    for i in range(9):
        block = xor_bytes(block, keys[i])
        block = bytes([pi0[b] for b in block])
        block = L(block)
    block = xor_bytes(block, keys[9])
    return block

def decrypt_block(block, keys):
    block = xor_bytes(block, keys[9])
    for i in range(8, -1, -1):
        block = L_inv(block)
        block = bytes([pi1[b] for b in block])
        block = xor_bytes(block, keys[i])
    return block

def pad_data(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad_data(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_data(data, key):
    keys = generate_round_keys(key)
    data = pad_data(data)
    encrypted = b''
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        encrypted += encrypt_block(block, keys)
    return encrypted

def decrypt_data(data, key):
    keys = generate_round_keys(key)
    decrypted = b''
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i+BLOCK_SIZE]
        decrypted += decrypt_block(block, keys)
    return unpad_data(decrypted)

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

if __name__ == "__main__":
    pi0, pi1 = generate_s_blocks()

    key = os.urandom(8)

    message = b"Hello, Kuznechik!"

    encrypted = encrypt_data(message, key)
    print("Encrypted:", encrypted)

    decrypted = decrypt_data(encrypted, key)
    print("Decrypted:", decrypted.decode())

    write_file("infsec/lab11/encrypted.bin", encrypted)
    encrypted_from_file = read_file("infsec/lab11/encrypted.bin")
    decrypted_from_file = decrypt_data(encrypted_from_file, key)
    print("Decrypted from file:", decrypted_from_file.decode())