import hashlib
import json
import requests
import time

# Configuration
API_URL = "https://bazcoin.org:5000"
MINER_WALLET_ID = input("Enter Your Wallet ID : ")

def get_last_block():
    """Fetch the last block from the blockchain."""
    response = requests.get(f"{API_URL}/block/last")
    if response.status_code == 200:
        return response.json()["block"]
    else:
        print(f"Error fetching last block: {response.text}")
        return None

def calculate_hash(index, previous_hash, timestamp, data, difficulty, nonce):
    """Calculate the hash of a block."""
    block_string = f"{index}{previous_hash}{timestamp}{data}{difficulty}{nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def mine_block():
    """Mine a new block."""
    last_block = get_last_block()
    if not last_block:
        print("No block available for mining.")
        return

    index = last_block["index"] + 1
    previous_hash = last_block["hash"]
    timestamp = time.time()
    difficulty = last_block["difficulty"]
    unconfirmed_transactions = json.loads(last_block["data"])

    # Block data including miner's ID
    data = json.dumps([{"miner": MINER_WALLET_ID},{"unconfirmed_transactions": unconfirmed_transactions}])

    nonce = 0
    start_time = time.time()
    while True:
        candidate_hash = calculate_hash(index, previous_hash, timestamp, data , difficulty , str(nonce))
        if candidate_hash.startswith("0" * difficulty):
            print(f"Block mined! Hash: {candidate_hash}")
            submit_block(index, previous_hash, timestamp, data , candidate_hash, difficulty , str(nonce))
            endtime = time.time()
            seconds = (endtime-start_time)
            if seconds!=0:
                hashrate = (nonce / seconds)/1000
                print("HashRate : "+str(("{:.2f}".format(hashrate)))+" KH/s")
            break
        nonce += 1

def submit_block(index, previous_hash, timestamp, data, block_hash, difficulty , nonce):
    """Submit the mined block to the API."""
    block_data = {
        "index": index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "data": data,
        "hash": block_hash,
        "difficulty": difficulty,
        "nonce": nonce
    }

    response = requests.post(f"{API_URL}/block/mine", json=block_data)
    if response.status_code == 201:
        print("Block successfully submitted!")
    else:
        print(f"Error submitting block: {response.text}")

if __name__ == "__main__":
    print("Starting mining process...")
    while True:
        mine_block()
