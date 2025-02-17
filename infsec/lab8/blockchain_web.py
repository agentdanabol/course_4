from flask import Flask, jsonify, request
import hashlib
import time

app = Flask(__name__)

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
        self.save_to_file()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.get_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def save_to_file(self, filename="infsec/lab8/blockchain_output.txt"):
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

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "nonce": block.nonce,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        })
    return jsonify(chain_data), 200

@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "Please provide 'data' in the request body"}), 400

    blockchain.add_block(data)
    return jsonify({
        "message": "New block mined!",
        "index": blockchain.get_last_block().index,
        "hash": blockchain.get_last_block().hash,
        "mining_time_ms": blockchain.mining_time_ms
    }), 201

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        return jsonify({"message": "Blockchain is valid!"}), 200
    else:
        return jsonify({"message": "Blockchain is invalid!"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)

# curl localhost:8088/chain
# curl -X POST -H "Content-Type: application/json" -d '{"data": "Your Data"}' localhost:8088/mine
# curl localhost:8088/validate
