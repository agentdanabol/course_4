import random

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def gf_mul(x, y, poly=0x187):
    result = 0
    for i in range(8):
        if y & 1:
            result ^= x
        hi_bit_set = x & 0x80
        x <<= 1
        if hi_bit_set:
            x ^= poly
        y >>= 1
    return result & 0xFF

def generate_sbox(seed):
    random.seed(seed)
    sbox = list(range(256))
    random.shuffle(sbox)
    inv_sbox = [0]*256
    for i, val in enumerate(sbox):
        inv_sbox[val] = i
    return sbox, inv_sbox

def R(state, poly=0x187):
    x = state[-1]
    new_state = [0]*len(state)
    for i in range(len(state)-1, 0, -1):
        new_state[i] = state[i-1]
        x ^= gf_mul(state[i-1], poly)
    new_state[0] = x
    return new_state

def L(block):
    state = list(block)
    for _ in range(len(block) * 8):
        state = R(state)
    return bytes(state)

def R_inv(state, poly=0x187):
    x = state[0]
    new_state = [0]*len(state)
    for i in range(len(state)-1):
        new_state[i] = state[i+1]
        x ^= gf_mul(new_state[i], poly)
    new_state[-1] = x
    return new_state

def L_inv(block):
    state = list(block)
    for _ in range(len(block) * 8):
        state = R_inv(state)
    return bytes(state)

def key_schedule(master_key, sbox):
    keys = []
    K1, K2 = master_key[:len(master_key)//2], master_key[len(master_key)//2:]
    keys.append(K1)
    keys.append(K2)
    for i in range(1, 5):
        c = i.to_bytes(len(K1), 'big')
        c = L(bytes(sbox[b] for b in c))
        K1 = xor_bytes(L(bytes(sbox[b] for b in xor_bytes(K1, c))), K2)
        K2 = K1
        keys.append(K1)
        keys.append(K2)
    return keys[:10]

def encrypt_block(block, keys, sbox):
    state = block
    for i in range(9):
        state = xor_bytes(state, keys[i])
        state = bytes(sbox[b] for b in state)
        state = L(state)
    return xor_bytes(state, keys[9])

def decrypt_block(block, keys, inv_sbox):
    state = xor_bytes(block, keys[9])
    for i in range(8, -1, -1):
        state = L_inv(state)
        state = bytes(inv_sbox[b] for b in state)
        state = xor_bytes(state, keys[i])
    return state

def pad(data, block_size):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    return data[:-data[-1]]

def process_file(input_path, output_path, key, mode='encrypt'):
    with open(input_path, 'rb') as f:
        data = f.read()

    block_size = 4
    sbox, inv_sbox = generate_sbox(sum(key))
    keys = key_schedule(key, sbox)

    if mode == 'encrypt':
        data = pad(data, block_size)
        result = b''.join(encrypt_block(data[i:i+block_size], keys, sbox) for i in range(0, len(data), block_size))
    else:
        blocks = [data[i:i+block_size] for i in range(0, len(data), block_size)]
        result = b''.join(decrypt_block(block, keys, inv_sbox) for block in blocks)
        result = unpad(result)

    with open(output_path, 'wb') as f:
        f.write(result)


key = b'0123456789abcdef'  # 16-byte key
process_file('infsec/lab11/input.txt', 'infsec/lab11/encrypted.bin', key, mode='encrypt')
process_file('infsec/lab11/encrypted.bin', 'infsec/lab11/decrypted.txt', key, mode='decrypt')
