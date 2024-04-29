from web3 import Web3
import json

with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)

bytecode = compiled_sol['contracts']['Interaction.sol']['Interaction']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['Interaction.sol']['Interaction']['abi']

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Set the default account
w3.eth.default_account = w3.eth.accounts[0]

# Create the contract in Python
Interaction = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Interaction.constructor().transact()

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Interact with the contract
contract_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(contract_instance.functions.getMyNumber().call())

# Update the contract state
tx_hash = contract_instance.functions.setMyNumber(255).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(contract_instance.functions.getMyNumber().call())