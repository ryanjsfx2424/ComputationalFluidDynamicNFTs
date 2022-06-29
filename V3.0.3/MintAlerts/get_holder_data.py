## get wallets holding BAYC
import os
import json
from web3 import Web3

DATA_DIR = "data4"
os.system("mkdir -p " + DATA_DIR)

ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY"]
ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/" + ALCHEMY_API_KEY
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

#INFURA_API_KEY = os.environ["INFURA_API_KEY"]
#INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY
#w3 = Web3(Web3.HTTPProvider(INFURA_URL))

wallets = []
nfts = { # data
    "bayc": {
        "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",
        "holders": []
    }
}
nfts = { # data 2
    "azuki": {
        "contract": "0xED5AF388653567Af2F388E6224dC7C4b3241C544",
        "holders": []
    }
}
nfts = { # data 3
    "moonbirds": {
        "contract": "0x23581767a106ae21c074b2276D25e5C3e136a68b",
        "holders": []
    }
}
nfts = { # data 6
    "cyberkongz": {
        "contract": "0x57a204AA1042f6E66DD7730813f4024114d74f37",
        "holders": []
    }
}
nfts = { # data 5
    "doodles": {
        "contract": "0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e",
        "holders": []
    }
}
nfts = { # data 4
    "mayc": {
        "contract": "0x60E4d786628Fea6478F785A6d7e704777c86a7c6",
        "holders": []
    }
}


fname = DATA_DIR + "/nfts.txt"
if os.path.exists(fname) and os.stat(fname).st_size != 0:
    with open(DATA_DIR + "/nfts.txt", "r") as fid:
        nfts = json.loads(fid.read().replace("'", '"'))
    # end with open
    print("nfts: ", nfts)
# end if

fname = DATA_DIR + "/wallets.txt"
if os.path.exists(fname) and os.stat(fname).st_size != 0:
    with open(fname, "r") as fid:
        wallets = fid.read()[1:-1].split(", ")
    # end with open
    print("wallets: ", wallets)
# end if

for nft in nfts:
    print("nft: ", nft)
    with open("ABIs/" + nft + ".txt", "r") as fid:
        abi = json.loads(fid.read())
    # end with open
    name = nft + ""
    nft = nfts[nft]
    contract = w3.eth.contract(address = nft["contract"], abi=abi)

    totalSupply = contract.functions.totalSupply().call()

    ## note all are 0-indexed except cyber-kongz 1-indexed
    start = 0
    end = totalSupply
    print("name: ", name)
    print(name == "cyberkongz")
    if name == "cyberkongz":
        start += 1
        end += 1
    # end if

    if   name == "mayc":
        start = 10002
    elif name == "doodles":
        start = 6777
    # end if

    for jj in range(start, end):
        print("jj: ", jj)
        try:
            wallet = contract.functions.ownerOf(jj).call()
        except Exception as err:
            print("err: ", err)
            print("err args: ", err.args[:])
            continue

        print("wallet: ", wallet)
        if wallet not in wallets:
            wallets.append(wallet)

            with open(DATA_DIR + "/wallets.txt", "w") as fid:
                fid.write(str(wallets))
            # end with open
        # end if
        
        if wallet not in nft["holders"]:
            nft["holders"].append(wallet)

            with open(DATA_DIR + "/nfts.txt", "w") as fid:
                fid.write(str(nfts))
            # end with open
        # end if
    # end for
# end for
print("nfts: ", nfts)
print("wallets: ", wallets)

with open(DATA_DIR + "/nfts.txt", "w") as fid:
    fid.write(str(nfts))
# end with open
with open(DATA_DIR + "/wallets.txt", "w") as fid:
    fid.write(str(wallets))
# end with open
