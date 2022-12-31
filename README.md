# Ethereum Blockchain Analysis

On-chain forensics tools for detecting sandwich attacks and tracking wallet activity on Ethereum.

## Tools

### Sandwich Attack Detector

Scans the latest Ethereum block for likely sandwich attacks by identifying repeated `from → to` address pairs within the same block and filtering out uniform-gas bot transactions.

**Requires:** A WebSocket provider URL (e.g. Infura, Alchemy).

```sh
export PROVIDER="wss://mainnet.infura.io/ws/v3/YOUR_KEY"
pip install web3
python SandwichAttacks/detectSandwichAttacksLive.py
```

### Wallet Tracker

Lists all transactions for a set of wallet addresses via the Etherscan API. For contract interactions, it decodes and displays the method ID, function signature, and input arguments. Also supports summing total account value from internal transactions.

**Requires:** An [Etherscan API key](https://etherscan.io/apis).

```sh
export etherscanAPI="YOUR_KEY"
python TrackWallets/trackWallets.py
```

Wallet addresses are currently hard-coded in `TrackWallets/trackWallets.py`. Edit the `WALLETS` list to track different addresses.

## Project Structure

```
SandwichAttacks/
  detectSandwichAttacksLive.py   # Sandwich attack detection against latest block
  requirements.txt
TrackWallets/
  trackWallets.py                # Wallet transaction listing and contract call decoding
```

## Dependencies

- Python 3
- [web3.py](https://github.com/ethereum/web3.py) (sandwich detector)
- [requests](https://pypi.org/project/requests/) (wallet tracker)

## Credits

Inspired by [ConsoleCowboys](https://www.youtube.com/@ConsoleCowboys) on YouTube.
