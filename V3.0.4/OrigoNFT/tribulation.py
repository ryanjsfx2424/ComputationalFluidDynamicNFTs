import os
import json
from web3 import Web3

CONTRACT = "0xa1f9f9dDE41319dBe124d80d0a2A2fC854667E16"
TRIB_ADDRESS = "0xC7d7Cc95DeD3B8C81f17AF0e65DEf2d4abB366f7"

INFURA_URL = os.environ["INFURA_RINK"]

with open("contract/rc6_abi.json", "r") as fid:
#with open("abi.json", "r") as fid:
  rl = "".join(fid.readlines())
  abi = json.loads(rl)
# end wwith

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=CONTRACT, abi=abi)
totalSupply = contract.functions.totalSupply().call()

tokenId = 6

transaction = contract.functions.tribulation(tokenId).buildTransaction({"from":TRIB_ADDRESS})
gas_estimate = w3.eth.estimateGas(transaction)

transaction.update({ "gas": int(1.2*gas_estimate) })
transaction.update({ "nonce": w3.eth.get_transaction_count(TRIB_ADDRESS) })
signed_tx = w3.eth.account.sign_transaction(transaction, os.environ["TRIB"])
print("signed_tx: ", signed_tx)

txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("txn_hash: ", txn_hash)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("txn_receipt: ", txn_receipt)

print("SUCCESS!")
