# Find Sandwich Attacks Live

This tool will look at the latest block and detect likely sandwich attacks.

- Inspiration taken from ConsoleCowboys on youtube

## Usage

To use this, please give it a websockets URL for a provider. An example one is Infura or Alchemy.

Note: if there are 0 bots or 0 attacks, just keep trying it does not mean the script does not work.

```python

export PROVIDER="wss://..."
python ./detectSandwichAttacksLive.py
```
