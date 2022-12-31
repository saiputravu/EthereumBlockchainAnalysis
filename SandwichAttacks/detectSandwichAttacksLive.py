import os
import sys
from typing import Union, List, Dict, Tuple
from web3 import Web3

PROVIDER_URL = os.environ.get("PROVIDER")
if not PROVIDER_URL:
    print("Error: PROVIDER environment variable is not set.", file=sys.stderr)
    sys.exit(1)

# Convert wss:// URLs to https:// since web3.py v7 WebSocketProvider requires AsyncWeb3
if PROVIDER_URL.startswith("wss://"):
    PROVIDER_URL = PROVIDER_URL.replace("wss://", "https://", 1).replace("/ws/", "/", 1)
elif PROVIDER_URL.startswith("ws://"):
    PROVIDER_URL = PROVIDER_URL.replace("ws://", "http://", 1).replace("/ws/", "/", 1)

provider = Web3(Web3.HTTPProvider(PROVIDER_URL))

def checkBlockForBots(block_id: Union[int, str]="latest") -> Dict[Tuple[str, str], Dict]:
    """
        This checks a given block for bots.
        It does this by checking the transactions with
         matching (from, to) address pairs.
        The transactions are likely made from bots if
         they are made within same block.

        Arguments:
            block_id: Passed onto provider. Block identifier.

        Return:
            addressMapping: A dictionary of (from, to) pairs to their
                             transaction data including tx list and indices.
    """
    block = provider.eth.get_block(block_id)
    addressMapping = {}

    if block and block.transactions:
        print(f"[!] Sorting through {len(block.transactions)} transactions")
        all_txs = []
        for idx, transaction in enumerate(block.transactions):
            tx_hash = transaction.hex()
            tx = provider.eth.get_transaction(tx_hash)
            all_txs.append({"tx": tx, "hash": tx_hash, "index": idx})

            if tx["to"] is None:
                continue

            key = (tx["from"], tx["to"])

            if key in addressMapping:
                addressMapping[key]["txs"].append(tx)
                addressMapping[key]["hashes"].append(tx_hash)
                addressMapping[key]["indices"].append(idx)
            else:
                addressMapping[key] = {
                    "from": tx["from"],
                    "to": tx["to"],
                    "txs": [tx],
                    "hashes": [tx_hash],
                    "indices": [idx],
                }

        # Store all transactions on the block for victim detection
        for entry in addressMapping.values():
            entry["all_block_txs"] = all_txs

    # Only keep pairs with more than one transaction (potential bot activity)
    addressMapping = {k: v for k, v in addressMapping.items() if len(v["txs"]) > 1}
    return addressMapping

def findPossibleSandwich(addressMapping: Dict[Tuple[str, str], Dict]) -> List[Dict]:
    """
        Checks the given addressMapping for possible sandwich
         transactions.
        A sandwich is detected when:
        - A bot sends 2+ transactions to the same target
        - At least one transaction from a different sender (the victim)
          exists between the bot's transactions by index position
    """

    possible_sandwich = []
    for entry in addressMapping.values():
        bot_from = entry["from"]
        bot_to = entry["to"]
        indices = entry["indices"]
        all_block_txs = entry["all_block_txs"]

        if len(indices) < 2:
            continue

        # Look for victim transactions between the first and last bot tx
        min_idx = min(indices)
        max_idx = max(indices)

        victims = []
        for tx_data in all_block_txs:
            idx = tx_data["index"]
            tx = tx_data["tx"]
            if min_idx < idx < max_idx:
                # Victim is a different sender targeting the same contract
                if tx["from"] != bot_from and tx["to"] == bot_to:
                    victims.append(tx_data)

        if victims:
            possible_sandwich.append({
                "bot_hashes": entry["hashes"],
                "victim_hashes": [v["hash"] for v in victims],
                "bot_from": bot_from,
                "target": bot_to,
            })

    return possible_sandwich

def main():
    sus_txs = checkBlockForBots()
    print(f"[+] Found {len(sus_txs)} possible bot transaction pairs")
    sandwichTransactions = findPossibleSandwich(sus_txs)

    if sandwichTransactions:
        print(f"[+] Found {len(sandwichTransactions)} possible sandwich attacks:")
        for s in sandwichTransactions:
            print(f"\tBot ({s['bot_from']}) -> Target ({s['target']})")
            print(f"\t  Front/Back-run: {s['bot_hashes']}")
            print(f"\t  Victim txs:     {s['victim_hashes']}")
    else:
        print("[+] No sandwich attacks detected in this block.")

if __name__ == "__main__":
    main()
