import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.get_hash()

    def get_hash(self):
        sha256 = hashlib.sha256()
        sha256.update(str(self.index).encode('utf-8'))
        sha256.update(self.previous_hash.encode('utf-8'))
        sha256.update(str(self.timestamp).encode('utf-8'))
        sha256.update(self.data.encode('utf-8'))
        sha256.update(str(self.nonce).encode('utf-8'))
        return sha256.hexdigest()

    def mine(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.get_hash()

class Blockchain:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]
        self.mining_time_ms = 0 

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(last_block.index + 1, last_block.hash, time.time(), data)

        start_time = time.time() * 1000  
        new_block.mine(self.difficulty)
        end_time = time.time() * 1000 

        self.mining_time_ms = end_time - start_time
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.get_hash():
                print("Current block hash is invalid!")
                return False

            if current_block.previous_hash != previous_block.hash:
                print("Previous block hash is invalid!")
                return False

        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.index} [")
            print(f"  Data: {block.data}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Hash: {block.hash}")
            print(f"  PrevHash: {block.previous_hash}")
            print("]")

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for block in self.chain:
                file.write(f"Block {block.index} [\n")
                file.write(f"  Data: {block.data}\n")
                file.write(f"  Timestamp: {block.timestamp}\n")
                file.write(f"  Nonce: {block.nonce}\n")
                file.write(f"  Hash: {block.hash}\n")
                file.write(f"  PrevHash: {block.previous_hash}\n")
                file.write("]\n")
            file.write(f"Mining time for last block: {self.mining_time_ms:.2f} ms\n")


blockchain = Blockchain(difficulty=4)
blockchain.add_block("First Block")
blockchain.add_block("Second Block")
blockchain.add_block("Third Block")
blockchain.add_block("Fourth Block")

blockchain.print_chain()
blockchain.save_to_file(filename="./infsec/lab8/blockchain_output.txt")

print("Blockchain valid:", blockchain.is_chain_valid())