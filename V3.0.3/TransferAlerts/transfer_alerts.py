#URL generator result:
# send messages
# embed links
# read messages / view channels
#https://discord.com/api/oauth2/authorize?client_id=992758539061821440&permissions=274877924352&scope=bot

import os
import ast
import glob
import time
import json
import asyncio
from web3 import Web3
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="./geckodriver")
OS_BASE = "https://opensea.io/assets/ethereum/"

class TransferAlerts(object):
    def __init__(self):
        self.CID = 932056137518444594
        self.transfer_data_fname = "transfer_data.txt"
        self.ICON_URL = "https://cdn.discordapp.com/attachments/932056137518444594/992768887890395166/Screenshot_2022-07-02_at_13.48.53.png"
    # end __init__

    async def get_holder_data(self):
        DATA_DIR = "data_"

        INFURA_API_KEY = os.environ["INFURA_API_KEY"]
        INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY
        w3 = Web3(Web3.HTTPProvider(INFURA_URL))

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

        nfts = { # data _proof
            "proof": {
                "contract": "0x08D7C0242953446436F34b4C78Fe9da38c73668d",
                "holders": []
            }
        }

        nfts = { # data _llamaverse
            "llamaverse": {
                "contract": "0x9df8Aa7C681f33E442A0d57B838555da863504f3",
                "holders": []
            }
        }

        nfts = { # data _pgodjira
            "pgodjira": {
                "contract": "0x9ada21A8bc6c33B49a089CFC1c24545d2a27cD81",
                "holders": []
            }
        }

        nfts = { # data _kaijukingz
            "kaijukingz": {
                "contract": "0x0c2E57EFddbA8c768147D1fdF9176a0A6EBd5d83",
                "holders": []
            }
        }

        DATA_DIR += list(nfts.keys())[0]
        os.system("mkdir -p " + DATA_DIR)


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
            if name in ["cyberkongz", "pgodjira"]:
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
        print(list(nfts.keys())[0])
    # end get_holder_data

    async def track_holder_transfers(self):
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
        self.nfts = nfts

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

        self.contracts = {}
        transfers = 0
        wcnt = 0
        num_blocks = 50
        while True:
            wcnt += 1
            new_block = w3.eth.get_block_number()

            url  = ETHERSCAN_URL + "?module=logs&action=getLogs"
            url += "&fromBlock=" + str(new_block-num_blocks)
            url += "&toBlock=latest"
            url += "&topic0=" + TRANSFER_HASH
            url += "&apikey=" + ETHERSCAN_API_KEY

            fname = FNAME + str(wcnt)
            #os.system("curl --request GET --url '" + url + "' > " + fname)
            with open(fname, "r") as fid:
                line = fid.read()
            # end with open
            line = ast.literal_eval(line)
            #print("line: ", line)

            if len(line["result"]) > 0:
                results = line["result"]
                for result in results:
                    for jj,addy in enumerate(result["topics"][1:]):
                        addy = "0x" + addy[2:].strip("0")
                        if addy in wallets:
                            contract = result["address"]
                            print("blue chip holder did a transfer!")
                            print(result["address"])
                            transfers += 1

                            transfer_type = ""
                            if jj == 0:
                                if len(result["topics"][2][2:].strip("0")) < 10:
                                    transfer_type = "burned"
                                else:
                                    transfer_type = "sold"
                                # end if/else
                            elif jj == 1:
                                if len(result["topics"][1][2:].strip("0")) < 3:
                                    transfer_type = "minted"
                                else:
                                    transfer_type = "bought"
                                # end if/else
                            # end if/else
                            if transfer_type == "":
                                print("transfer type still none??")
                                print("line: ", line)
                                raise
                            # end if

                            blue = ""
                            for nft in nfts.keys():
                                if addy in nfts[nft]["holders"]:
                                    blue = nft
                                # end if
                            # end for

                            if contract not in self.contracts:
                                self.contracts[contract] = {"times":[], "blues":[], "types":[]}
                            # end if/else
                            self.contracts[contract]["times"].append(time.time())
                            self.contracts[contract]["blues"].append(blue)
                            self.contracts[contract]["types"].append(transfer_type)

                            with open(self.transfer_data_fname, "w") as fid:
                                fid.write(str(self.contracts))
                            # end with open
                        # end if
                    # end for
                # end for
            # end if

            msg = str(transfers) + " tracked holders bought, sold, minted or burned"
            msg += " in the past " + str(num_blocks*15) + " seconds"
            print(msg)
            break
            await asyncio.sleep(10)
        # end while
        print("SUCCESS")
    # end def track_holder_transfers

    async def alert_on_transfer(self, client):
        channel = client.get_channel(self.CID)

        while True:
            for contract in self.contracts:
                os_url = OS_BASE + contract + "/1"
                driver.get(os_url)
                html_source = driver.page_source
                try:
                    collection = html_source.split('CollectionLink--link" href="')[1].split('"')[0]
                except Exception as err:
                    print("err 290: ", err)
                    print("err.args 290: ", err.args[:])
                    continue
                # end try/except
                name = html_source.split('CollectionLink--link" href="')[1].split(
                    "<div class=")[1].split(">")[1].split("<")[0]
                collection_url = "https://opensea.io" + collection

                transfer_type = self.contracts[contract]

                description = ""
                for jj in range(len(self.contracts[contract]["times"])):

                    blue  = self.contracts[contract]["blues"][jj]
                    ttype = self.contracts[contract]["types"][jj]

                    if jj > 0:
                        description = description[:-1] + ", "
                    # end if
                    description += "1 " + ttype + " by a " + blue + " holder."
                # end for jj

                #embed = discord.Embed(title = name, description = "Transfer from a blue chip holder.")
                embed = discord.Embed(title = name, description = description)
                embed.set_footer(text = "Build for NFT Round Table, Powered by @TheLunaLabs", 
                    icon_url=self.ICON_URL)
                embed.set_thumbnail(url = self.ICON_URL)
                embed.add_field(name = "OpenSea", value = collection_url, inline=False)
                embed.add_field(name = "Contract Address", value = "https://etherscan.io/token/" + contract, inline=False)
                embed.add_field(name = "Blue Chips Tracked", value = ", ".join(list(self.nfts.keys())))
                await channel.send(embed=embed)
            # end for contracts
            break
        # end while
    # end alert_on_transfers
        
            

    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            await self.track_holder_transfers()
            await self.alert_on_transfer(client)
        # end on_ready

        client.run(os.environ.get("taBotPass"))
    # end discord_bot
# end TransferAlerts

if __name__ == "__main__":
    ta = TransferAlerts()
    ta.discord_bot()
# end if
## end transfer_alerts.py