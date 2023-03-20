from web3 import Web3
import time
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
from eth_account import Account
w3=Web3(Web3.HTTPProvider(os.environ.get('RPC'))) #RPC
with open('abi.json', 'r') as f:
    contract_abi = json.load(f)

def send(key,reciever):
    print(key)
    print(reciever)
    acct = Account.from_key(key)
    contract_address = '0x912CE59144191C1204E64559FE8253a0e49E6548' #Arbitrum Contract Address
    token_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    token_balance = token_contract.functions.balanceOf(acct.address).call()
    print(token_balance);
    if token_balance > 0:
        nonce=w3.eth.getTransactionCount(acct.address);
        tx = {
        'from':acct.address,
        'chainId':42161,
        'nonce': nonce,
        'to': contract_address,
        'data':'a9059cbb' + reciever[2:].rjust(64, '0') + hex(token_balance)[2:].rjust(64, '0'),
        'gas': 1000000,
        'value': w3.toWei(0,'ether'),
        'gasPrice': w3.toWei(0.1, 'gwei')
        }
        signedTx2 = w3.eth.account.signTransaction(tx, key);
        w3.eth.sendRawTransaction(signedTx2.rawTransaction);

while True:
    try:
        send(os.environ.get('PRIVATE_KEY'),os.environ.get('SAFE_ADDRESS'));
    except:
        print("Error Transfer I will try again...");
