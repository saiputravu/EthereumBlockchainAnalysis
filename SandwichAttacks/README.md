# Find Sandwich Attacks Live

This tool will look at the latest block and detect likely sandwich attacks.

- Inspiration taken from ConsoleCowboys on youtube

## How it works

1. Fetches all transactions in the latest (or specified) block
2. Groups transactions by `(from, to)` address pair to identify bots sending multiple txs to the same contract
3. For each bot pair, checks if a victim transaction from a different sender exists between the front-run and back-run by transaction index
4. Reports matching patterns as possible sandwich attacks

## Usage

Provide an Ethereum provider URL. Both HTTPS and WSS URLs are supported (WSS is auto-converted to HTTPS internally).

```sh
export PROVIDER="https://mainnet.infura.io/v3/YOUR_KEY"
python ./detectSandwichAttacksLive.py
```

Note: if there are 0 bots or 0 attacks, just keep trying it does not mean the script does not work.
