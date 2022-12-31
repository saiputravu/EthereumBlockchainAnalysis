# Ethereum Blockchain Analysis

On-chain forensics tools for detecting sandwich attacks and tracking wallet activity on Ethereum.

## Tools

### Sandwich Attack Detector

Scans the latest Ethereum block for likely sandwich attacks by identifying repeated `(from, to)` address pairs within the same block, then checking for victim transactions positioned between the bot's front-run and back-run by transaction index.

**Requires:** An Ethereum provider URL (e.g. Infura, Alchemy). Both HTTPS and WSS URLs are supported (WSS is auto-converted to HTTPS internally).

```sh
export PROVIDER="https://mainnet.infura.io/v3/YOUR_KEY"
pip install web3
python SandwichAttacks/detectSandwichAttacksLive.py
```

### Wallet Tracker

Lists all transactions for a set of wallet addresses via the Etherscan V2 API. For contract interactions, it decodes and displays the method ID, function signature, and input arguments. Also supports summing total account value from both normal and internal transactions, with direction-aware accounting (inflows added, outflows subtracted).

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
