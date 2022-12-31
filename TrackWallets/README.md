# Track Wallets

This project is interesting, I tried looking for scammers who try and trick innocent users to deploy malicious contracts. 
This code essentially tracks their wallet addresses' transactions as well as tally up the total account balance.

This project tracks wallets and transactions using the Etherscan V2 API. If the transaction is made to a contract, it enumerates the function and its arguments. The `sumAccounts` function sums both normal and internal transactions with direction-aware accounting (inflows added, outflows subtracted).

Note: Still work in progress, I have hard-coded addresses.

- Inspiration from ConsoleCowboys on Youtube

## Usage

Make sure to add the etherscan API key for your account.

```python
export etherscanAPI="<apikeyhere>"
python ./trackWallets.py
```

## Output

```bash

[Wallet 0xb0a10bef7b0c4a4864a21e88f2039c2f5a1c38e7]
	[From 0xb0a10bef7b0c4a4864a21e88f2039c2f5a1c38e7 To 0x0c4aed959b42ef1086fb752e350afa88bb4a960f] : 0.109662954195464 Ether
	[From 0xb0a10bef7b0c4a4864a21e88f2039c2f5a1c38e7 To 0x862178f494c150eace18a5fc45b9fcfd2c1a36d2] : 0.999586587901201 Ether
	[From 0xb0a10bef7b0c4a4864a21e88f2039c2f5a1c38e7 To 0x46730e65c56d3ddd1cb611bfbd2cc1c77f281259] : 0.0442 Ether
	[From 0xb0a10bef7b0c4a4864a21e88f2039c2f5a1c38e7 To 0x530b827d8ddd4bde5d4df88b8f4e49ac3fd51549] : 0.438015140027171 Ether
[Wallet 0x386a4a06b477bc49e8bc75618aa1219cd82f0ba6]
	[From 0x386a4a06b477bc49e8bc75618aa1219cd82f0ba6 To 0x8411204f8551d3a73f008b9268ddf7c2da7189fb] : 10.01761532343192 Ether
[Wallet 0x274ebddc9d9aac7d60d03b7f013ede0db515af8f]
	[From 0x274ebddc9d9aac7d60d03b7f013ede0db515af8f To 0xbb7ed895abd31b3e5af0b06f72bd4e706db21790] : 13.606541460382987 Ether
[Wallet 0x85fab391aa46f8c24e6aa10a94981023b6a8b656]
	[From 0x85fab391aa46f8c24e6aa10a94981023b6a8b656 To 0xba8da9dcf11b50b03fd5284f164ef5cdef910705] : 17.4598297 Ether
		Method ID        : 0xa5e56571
		Function Name    : anySwapOutNative(address token, address to, uint256 toChainID)
		Input Data[3] 
			[0] : 0000000000000000000000000615dbba33fe61a31c7ed131bda6655ed76748b1
			[1] : 000000000000000000000000c0ca4fb1f0c4d027e7dab250954c24fdb9332270
			[2] : 0000000000000000000000000000000000000000000000000000000000000038
[Wallet 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c]
	[From 0x5d63e598b0c08201a6aee4694cd5c5d5e7d7093c To 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c] : 0.0 Ether
		Method ID        : 0xd4e93292
		Function Name    : withdrawal()
		Input Data[0] 
	[From 0x5d63e598b0c08201a6aee4694cd5c5d5e7d7093c To 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c] : 0.0 Ether
		Method ID        : 0xd4e93292
		Function Name    : withdrawal()
		Input Data[0] 
	[From 0x5d63e598b0c08201a6aee4694cd5c5d5e7d7093c To 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c] : 0.0 Ether
		Method ID        : 0xd4e93292
		Function Name    : withdrawal()
		Input Data[0] 
	[From 0x5d63e598b0c08201a6aee4694cd5c5d5e7d7093c To 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c] : 0.0 Ether
		Method ID        : 0xbe9a6555
		Function Name    : start()
		Input Data[0] 
	[From 0x5d63e598b0c08201a6aee4694cd5c5d5e7d7093c To 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c] : 0.0 Ether
		Method ID        : 0xd4e93292
		Function Name    : withdrawal()
		Input Data[0] 
	[From 0x143cbe2941569fe2fed6ce04bbe9281d03f0060c To 0xba8da9dcf11b50b03fd5284f164ef5cdef910705] : 12.4662818 Ether
		Method ID        : 0xa5e56571
		Function Name    : anySwapOutNative(address token, address to, uint256 toChainID)
		Input Data[3] 
			[0] : 0000000000000000000000000615dbba33fe61a31c7ed131bda6655ed76748b1
			[1] : 000000000000000000000000c0ca4fb1f0c4d027e7dab250954c24fdb9332270
			[2] : 0000000000000000000000000000000000000000000000000000000000000038
[Wallet 0x0fbcc615ac3f335e11e3472679070d73bd1bba63]
	[From 0x0fbcc615ac3f335e11e3472679070d73bd1bba63 To 0xba8da9dcf11b50b03fd5284f164ef5cdef910705] : 14.8980809 Ether
		Method ID        : 0xa5e56571
		Function Name    : anySwapOutNative(address token, address to, uint256 toChainID)
		Input Data[3] 
			[0] : 0000000000000000000000000615dbba33fe61a31c7ed131bda6655ed76748b1
			[1] : 000000000000000000000000c0ca4fb1f0c4d027e7dab250954c24fdb9332270
			[2] : 0000000000000000000000000000000000000000000000000000000000000038
```
