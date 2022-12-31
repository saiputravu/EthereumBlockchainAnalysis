import os
from typing import Union, List, Dict
from web3 import Web3
from pprint import pprint

provider = Web3(Web3.WebsocketProvider(os.environ["PROVIDER"]))

def checkBlockForBots(block_id: Union[int, str]="latest") -> Dict[str, List]:
    """
        This checks a given block for bots. 
        It does this by checking the transactions with 
         matching to and from addresses.
        The transactions are likely made from bots if 
         they are made within same block.

        Arguments:
            block_id: Passed onto provider. Block identifier. 

        Return:
            addressMapping: A dictionary of to addresses to their 
                             from address and list of transactions
    """
    block = provider.eth.get_block("latest")
    addressMapping = {}
    
    if block and block.transactions:
        print(f"[!] Sorting through {len(block.transactions)} transactions")
        for transaction in block.transactions:
            tx_hash = transaction.hex()
            tx = provider.eth.get_transaction(tx_hash)
            
            try:
                # Already mapped pair, add the transaction hash
                if addressMapping[tx["to"]][0] == tx["from"]:
                    addressMapping[tx["to"]][1].append(tx)
                    addressMapping[tx["to"]][2].append(tx_hash)

            except KeyError:
                addressMapping[tx["to"]] = [
                    tx["from"],
                    [tx],
                    [tx_hash]
                ]

    addressMapping = {k:v for k,v in addressMapping.items() if len(v[1]) > 1}
    return addressMapping

def findPossibleSandwich(addressMapping: Dict[str, List]) -> List[str]:
    """
        Checks the given addressMapping for possible sandwich
         transactions.
        It does this by eliminating bots that send transactions
         with same gas value
    """

    possible_sandwich = []
    for value in addressMapping.values():
        transactions = value[1]

        gasValues = [tx["gas"] for tx in transactions]
        
        if len(set(gasValues)) > 1:
            # Append the pair of transactions
            # That are in the sandwich attack
            possible_sandwich.append(value[2])

    return possible_sandwich

def main():
    sus_txs = checkBlockForBots()
    print(f"[+] Found {len(sus_txs)} possible bot transactions")
    sandwichTransactions = findPossibleSandwich(sus_txs)
    

    if len(sus_txs):
        print(f"[+] Found transaction hashes of possible attacks:")
        for s in sandwichTransactions:
            print(f"\t[{s[0]}] --> [{s[1]}]")

if __name__ == "__main__":
    main()
