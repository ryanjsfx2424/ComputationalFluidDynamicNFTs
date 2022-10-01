import os
import time
from web3 import Web3
import numpy as np

fname1 = "RDH_Academy_PREMINT_Winners_List.csv"
fname2 = "Rekted_Diamond_Hands_PREMINT_Winners_List.csv"

WEI_PER_ETH = 1e18

w3 = Web3(Web3.HTTPProvider(os.environ["INFURA_ETH"]))

balances = []
wallets  = []
start = time.time()
for fname in [fname1,fname2]:
  print("fname: ", fname)

  with open(fname1, "r") as fid:
    lines = fid.readlines()[1:]
  # end with

  for line in lines:
    wallet = line.split(",")[0]
    wallets.append(wallet)

    balance = w3.eth.get_balance(Web3.toChecksumAddress(wallet)) / WEI_PER_ETH
    print("balance for addy: ", balance, wallet)
    print(time.time() - start)
    balances.append(balance)

  # end for
# end for
print("executed in: ", time.time() - start)
balances = np.array(balances)
wallets = np.array(wallets)

inds = np.argsort(balances)
balances = balances[inds]
wallets = wallets[inds]

with open("Premint_walletsByBalance.txt", "w") as fid:
  for ii in range(len(wallets)):
    print("ii: ", ii)
    fid.write(wallets[ii] + "," + str(balances[ii]) + " eth\n")
  # end for
# end with open
