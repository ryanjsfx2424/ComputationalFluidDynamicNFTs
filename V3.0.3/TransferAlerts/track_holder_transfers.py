## track_holder_transfers
import os
import glob
import ast
import time
from web3 import Web3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")

OS_BASE = "https://opensea.io/assets/ethereum/"

os_url = OS_BASE + contract + "/1"
                    driver.get(os_url)
                    html_source = driver.page_source
                    try:
                        collection = html_source.split('CollectionLink--link" href="')[1].split('"')[0]
                    except:
                        collection = "not on opensea!"
                    # end try/except

FNAME = "BLOCK_DATA/block_log_data.txt"

data_dirs = glob.glob("WALLETS/data_*")
nfts = {}
wallets = []
for data_dir in data_dirs:
    with open(data_dir + "/nfts.txt", "r") as fid:
        nft_data = ast.literal_eval(fid.read())
        nft = list(nft_data.keys())[0]
        nfts[nft] = nft_data[nft]
        for jj,wallet in enumerate(nft_data[nft]["holders"]):
            wallets.append(wallet.lower())
            nfts[nft]["holders"][jj] = wallet.lower()
        print("nft, num_wallets: ", nft, len(nft_data[nft]["holders"]))
    # end with
# end for data_dirs

ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]


## keccak256(Transfer(address,address,uint256)) ->
TRANSFER_HASH = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

ETHERSCAN_URL = "https://api.etherscan.io/api"

#ALCHEMY_API_KEY = os.environ["ALCHEMY_API_KEY"]
#ALCHEMY_URL = "https://eth-mainnet.alchemyapi.io/v2/" + ALCHEMY_API_KEY
#w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

INFURA_API_KEY = os.environ["INFURA_API_KEY"]
INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

contracts = {}
transfers = 0
wcnt = 0
num_blocks = 25
while True:
    wcnt += 1
    new_block = w3.eth.get_block_number()

    url  = ETHERSCAN_URL + "?module=logs&action=getLogs"
    url += "&fromBlock=" + str(new_block-num_blocks)
    url += "&toBlock=latest"
    url += "&topic0=" + TRANSFER_HASH
    url += "&apikey=" + ETHERSCAN_API_KEY

    fname = FNAME + str(wcnt)
    os.system("curl --request GET --url '" + url + "' > " + fname)
    with open(fname, "r") as fid:
        line = fid.read()
    # end with open
    line = ast.literal_eval(line)
    #print("line: ", line)

    if len(line["result"]) > 0:
        results = line["result"]
        for result in results:
            for addy in result["topics"][1:]:
                addy = "0x" + addy[2:].strip("0")
                if addy in wallets:
                    contract = result["address"]
                    print("blue chip holder did a transfer!")
                    print(result["address"])
                    transfers += 1

                    if contract not in contracts:
                        contracts[result["address"]] = 1
                    else:
                        contracts[result["address"]] += 1
                    # end if/else

                    #resp = requests.get()
                # end if
            # end for
        # end for
    # end if

    msg = str(transfers) + " tracked holders bought, sold, minted or burned"
    msg += " in the past " + str(num_blocks*15) + " seconds"
    print(msg)
    break
    time.sleep(10)
# end while
print("SUCCESS")