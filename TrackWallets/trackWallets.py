import os
import sys

import requests

API_KEY = os.environ.get("etherscanAPI")
if not API_KEY:
    print("Error: etherscanAPI environment variable is not set.", file=sys.stderr)
    sys.exit(1)

WALLETS = [
    "0xb0A10BeF7B0C4A4864A21e88f2039C2f5a1c38E7",
    "0x386a4a06B477BC49E8bc75618aA1219Cd82f0ba6",
    "0x274EbDDC9d9Aac7D60d03b7F013EDE0DB515af8f",
    "0x85faB391Aa46f8C24e6Aa10a94981023B6A8B656",
    "0x143cBE2941569fE2FeD6CE04BBE9281d03f0060c",
    "0x0FBCc615AC3f335e11e3472679070d73BD1Bba63",
]

class bcolors:
    """
        From 
        https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def queryApi(params: dict) -> list:
    url = "https://api.etherscan.io/v2/api"

    params["apikey"] = API_KEY
    params["chainid"] = 1  # Ethereum mainnet
    response = requests.get(url, params=params).json()

    if response.get("status") == "0":
        print(f"[!] Etherscan API error: {response.get('message', 'Unknown')} - {response.get('result', '')}", file=sys.stderr)
        return []

    return response["result"]


def sumAccounts(wallets: list) -> None:
    total = 0
    for address in wallets:
        account_sum = 0
        address_lower = address.lower()

        # Sum normal (external) transactions
        normal_txs = queryApi({
            "module": "account",
            "action": "txlist",
            "address": address,
            "sort": "asc",
        })
        for transaction in normal_txs:
            if transaction["isError"] == '0':
                value = int(transaction["value"])
                if transaction["from"].lower() == address_lower:
                    account_sum -= value
                else:
                    account_sum += value

        # Sum internal (contract-to-contract) transactions
        internal_txs = queryApi({
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "sort": "asc",
        })
        for transaction in internal_txs:
            if transaction["isError"] == '0':
                value = int(transaction["value"])
                if transaction["from"].lower() == address_lower:
                    account_sum -= value
                else:
                    account_sum += value

        # Wei to Eth conversion
        account_sum /= pow(10, 18)
        total += account_sum
        print(f"[{bcolors.WARNING}{address}{bcolors.ENDC}] : {bcolors.OKGREEN}{account_sum} Ether{bcolors.ENDC}")

    print()
    print(f"[{bcolors.UNDERLINE}{bcolors.FAIL}Total{bcolors.ENDC}] {bcolors.OKGREEN}{total} Ether{bcolors.ENDC}")

def listAccounts(wallets: list) -> None:
    for address in wallets:
        print(f"[{bcolors.FAIL}Wallet{bcolors.ENDC} {bcolors.OKCYAN}{address}{bcolors.ENDC}]")

        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "sort": "asc",
        }

        transactions = queryApi(params)
        for transaction in transactions:
            print(f'\t[From {bcolors.WARNING}{transaction["from"]}{bcolors.ENDC} To {bcolors.WARNING}{transaction["to"]}{bcolors.ENDC}] : {bcolors.OKGREEN}{int(transaction["value"])/pow(10,18)} Ether{bcolors.ENDC}')
            if len(transaction["input"]) > 2:

                # Check input format is correct
                inp = transaction["input"]
                methodId = inp[:10]
                if methodId != transaction["methodId"]:
                    raise Exception(f"MethodID and Transaction not matched for {transaction}")
                inp = inp[10:]

                # Generate Method arguments
                function_arguments = [inp[i:i+64] for i in range(0, len(inp), 64)]

                print(f'\t\t{bcolors.OKCYAN}Method ID{bcolors.ENDC}        : {transaction["methodId"]}')
                print(f'\t\t{bcolors.OKCYAN}Function Name{bcolors.ENDC}    : {transaction["functionName"]}')
                print(f'\t\t{bcolors.OKCYAN}Input Data[{int(len(inp)/64)}] {bcolors.ENDC}')
                for c, arg in enumerate(function_arguments):
                    print(f"\t\t\t[{c}] : {arg}")


def main() -> None:
    # sumAccounts(WALLETS)
    listAccounts(WALLETS)

if __name__ == "__main__":
    main()
