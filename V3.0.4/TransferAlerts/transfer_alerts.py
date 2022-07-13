import os
import ast
import glob
import time
import json
import socket
import numpy as np
import asyncio
import gspread
from web3 import Web3
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

exec_path = "/root/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver_linux"
if socket.gethostname() == "MB-145.local":
  exec_path = "/Users/ryanjsfx/Documents/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver"
driver = webdriver.Firefox(options=options, executable_path=exec_path)
OS_BASE = "https://opensea.io/assets/ethereum/"

class TransferAlerts(object):
    def __init__(self):
        self.QS = 0.001 # quick sleep
        self.LS = 10 # quick sleep
        self.dev_mode = True

        self.CID_LOG = 932056137518444594
        self.CID_MSG = 995421075414450186 # spy-tool in NFT Round Table
        #self.CID_MSG = 932056137518444594 # for testing
        self.ICON_URL = "https://cdn.discordapp.com/attachments/932056137518444594/992768887890395166/Screenshot_2022-07-02_at_13.48.53.png"

        self.wallet_path = "data_big/WALLETS"
        self.abi_path = "data_big/ABIS"
        self.transfers_path = "data_big/BLOCK_DATA"

        self.processed_fs_path = "data_big/processed_data.txt"

        self.init_gsheet()
        self.init_w3()
        self.init_processed_fs()
    # end __init__

    def init_gsheet(self):
        gc = gspread.service_account()
        sh = gc.open("TransferAlertSettings")
        self.worksheet = sh.get_worksheet(0)
    # end init_gsheet

    def init_w3(self):
        INFURA_API_KEY = os.environ["INFURA_API_KEY"]
        INFURA_URL = "https://mainnet.infura.io/v3/" + INFURA_API_KEY
        self.w3 = Web3(Web3.HTTPProvider(INFURA_URL))

        self.ETHERSCAN_API_KEY = os.environ["ETHERSCAN_API_KEY"]
        self.ETHERSCAN_URL = "https://api.etherscan.io/api"
        self.TRANSFER_HASH = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    # end init_w3

    def init_processed_fs(self):
        self.processed_fs = []
        ## load from where I save it if it exists
        fname = self.processed_fs_path
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                line = fid.read()
            # end with
            line = line.replace("\n","")
            if ", " in line:
                self.processed_fs = line.split(", ")
            else:
                self.processed_fs = [line]
            # end if/else
        # end if
    # end init_processed_fs

    async def get_settings(self):
        try:
          gsheet = self.worksheet.get_all_values()
        except Exception as err:
          print("83 err: ", err)
          print("84 err.args: ", err.args[:])
          msg = "error getting gsheet!"
          print(msg)
          await self.channel_log.send(msg)
          return
        # end try/except

        flag = False
        settings = {"collections"  :[],
                    "num_blocks"   :[],
                    "num_transfers":[],
                    "transaction_types":[]
                    }
        for row in gsheet:
            if "END DATA" in row:
                break
            elif flag:
                collection = row[0].lower()
                if collection not in self.nfts and collection not in ["any", "all"]:
                    msg = "warning! collection for row `" + str(row) + "` not in self.nfts so we're skipping"
                    msg += "\nnfts: " + ", ".join(list(self.nfts.keys()))
                    print(msg)
                    await self.channel_log.send(msg)
                    raise
                    continue
                # end if
                try:
                    num_blocks = float(row[1])/15.0
                except:
                    msg = "warning! exception getting num_blocks for row `" + row + "` so we're skipping"
                    print(msg)
                    await self.channel_log.send(msg)
                    raise
                    continue
                # end try/except
                try:
                    num_transfers = float(row[2])
                except:
                    msg = "warning! exception getting num_transfers for row `" + row + "` so we're skipping"
                    print(msg)
                    await self.channel_log.send(msg)
                    raise
                    continue
                # end try/except
                try:
                    transaction_type = row[3].lower()
                    if transaction_type not in ["bought", "sold", "minted", "burned", "all"]:
                        msg  = "warning! transaction_type not in 'bought',"
                        msg += "'sold', 'minted', 'burned', recvd: " + transaction_type
                        print(msg)
                        await self.channel_log.send(msg)
                        raise
                        continue
                    # end if
                except:
                    msg = "warning! exception getting transaction_type for row `" + row + "` so we're skipping"
                    print(msg)
                    await self.channel_log.send(msg)
                    raise
                    continue
                # end try/except

                settings["collections"  ].append(collection)
                settings["num_blocks"   ].append(num_blocks)
                settings["num_transfers"].append(num_transfers)
                settings["transaction_types"].append(transaction_type)
            elif "Time Window (seconds)" in row:
                flag = True
            # end if/elifs
        # end for row in gsheet
        self.settings = settings
    # end get_settings

    ## note, I haven't tested the re-write yet...
    async def get_holder_data(self, collection_name, contract):
        w3 = self.w3

        wallets = []
        nfts = {
            collection_name: 
            {
                "contract":contract,
                "holders":[]
            }
        }
        wallet_path = self.wallet_path + collection_name
        os.system("mkdir -p" + wallet_path)

        fname = wallet_path + "/nfts.txt"
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                nfts = json.loads(fid.read().replace("'", '"'))
            # end with open
            print("nfts: ", nfts)
        # end if

        fname = wallet_path + "/wallets.txt"
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                wallets = fid.read()[1:-1].split(", ")
            # end with open
            print("wallets: ", wallets)
        # end if

        for nft in nfts:
            await asyncio.sleep(self.QS)
            print("nft: ", nft)
            with open(self.abi_path + "/" + nft + ".txt", "r") as fid:
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
            if name in ["cyberkongz", "pgodjira"]:
                start += 1
                end += 1
            # end if

            for jj in range(start, end):
                await asyncio.sleep(self.QS)
                print("jj: ", jj)
                try:
                    wallet = contract.functions.ownerOf(jj).call()
                except Exception as err:
                    await channel_log.send("error grabbing wallet for jj = " + str(jj))
                    print("172 err: ", err)
                    print("173 err args: ", err.args[:])
                    continue

                print("wallet: ", wallet)
                if wallet not in wallets:
                    wallets.append(wallet)

                    with open(wallet_path + "/wallets.txt", "w") as fid:
                        fid.write(str(wallets))
                    # end with open
                # end if
                
                if wallet not in nft["holders"]:
                    nft["holders"].append(wallet)

                    with open(wallet_path + "/nfts.txt", "w") as fid:
                        fid.write(str(nfts))
                    # end with open
                # end if
            # end for
        # end for
        print("nfts: ", nfts)
        print("wallets: ", wallets)

        with open(wallet_path + "/nfts.txt", "w") as fid:
            fid.write(str(nfts))
        # end with open
        with open(wallet_path + "/wallets.txt", "w") as fid:
            fid.write(str(wallets))
        # end with open
        print(list(nfts.keys())[0])
    # end get_holder_data

    async def load_holder_data(self):
        data_dirs = glob.glob(self.wallet_path + "/*")
        nfts = {}
        wallets = []
        for data_dir in data_dirs:
            await asyncio.sleep(self.QS)
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
        self.wallets = wallets
    # end load_holder_data

    async def get_transfer_data(self, old_block, block):
        print("begin get_transfer_data")
        print("old_block: ", old_block)
        print("block: ", block)

        fname = self.transfers_path + "/block_log_data_from" + old_block \
              + "_to" + block + ".txt"

        url = self.ETHERSCAN_URL + "?module=logs&action=getLogs"
        url += "&fromBlock=" + old_block
        url += "&toBlock=latest"
        url += "&topic0=" + self.TRANSFER_HASH
        url += "&apikey=" + self.ETHERSCAN_API_KEY

        command = "curl --request GET --url '" + url + "'"
        #command += " --connect-timeout 30 --max-time 30"
        command += " > " + fname

        os.system(command)

        if self.dev_mode:
            os.system("cp " + fname + " " + fname + "_backup")
        # end if

        print("success get_transfer_data")
    # end get_transfer_data

    async def process_transfer_data(self):
        fs = glob.glob(self.transfers_path + "/*")
        for fname in fs:
            if "_backup" in fname:
                continue
            # end if
            print("fname: ", fname)

            if fname in self.processed_fs:
                os.system("rm " + fname)
                continue
            # end if

            recent_transfers = {
                "contracts": [],
                "transfer_types": [],
                "wallets": [],
                "blockNos": [],
                "blueChipHoldings": {}
            }
            for nft in self.nfts:
                recent_transfers["blueChipHoldings"][nft] = []
            # end for

            with open(fname, "r") as fid:
                line = fid.read()
            # end with open

            try:
                line = ast.literal_eval(line)
            except Exception as err:
                print("319 err: ", err)
                print("320 err.args: ", err.args)
                os.system("rm " + fname)
                continue
            # end try/except


            if not len(line["result"]) > 0:
                print("results nonpositive so continuing")
                os.system("rm " + fname)
                continue
            # end if

            results = line["result"]
            for result in results:
                for jj,addy in enumerate(result["topics"][1:]):
                    addy = "0x" + addy[2:].strip("0")
                    if addy in self.wallets:
                        print("blue chip holder did a transfer!")
                        print(result["address"])

                        recent_transfers["wallets"].append(addy)

                        recent_transfers["contracts"].append(
                            result["address"])

                        recent_transfers["blockNos"].append(
                            int(result["blockNumber"],0))

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
                            print("result[topics]: ", result["topics"])
                            raise
                        # end if
                        recent_transfers["transfer_types"].append(transfer_type)

                        ## which collection does this addy hold
                        for nft in self.nfts:
                            if addy in self.nfts[nft]["holders"]:
                                recent_transfers["blueChipHoldings"][nft].append(1)
                            else:
                                recent_transfers["blueChipHoldings"][nft].append(0)
                            # end if
                        # end for
                    # end if
                # end for topics
            # end for results
            cur_block = int(float(fname.split("_to")[1].replace(".txt","")))
            await self.process_recent_transfers(recent_transfers, cur_block)

            self.processed_fs.append(fname)
            with open(self.processed_fs_path, "w") as fid:
                fid.write(", ".join(self.processed_fs))
            # end with open

            os.system("rm " + fname)
            os.system("rm " + fname + "_backup")
        # end for fnames
    # end process_transfer_data

    async def process_recent_transfers(self, recent_transfers, cur_block):
        ## here is where we check for alerts to make
        for contract in list(set(recent_transfers["contracts"])):
            indsC = np.where(np.array(recent_transfers["contracts"])
                 == contract)

            test_tuple = (1,)
            if type(indsC) == type(test_tuple):
                indsC = indsC[0]
            # end if

            for jj in range(len(self.settings["collections"])):
                collection = self.settings["collections"  ][jj]
                threshold  = self.settings["num_transfers"][jj]
                num_blocks = self.settings["num_blocks"   ][jj]
                transaction_type = self.settings["transaction_types"][jj]

                print("indsC: ", indsC)
                indsB = np.where(np.array(recent_transfers["blockNos"])[indsC]
                        >= cur_block-num_blocks)
                if type(indsB) == type(test_tuple):
                    indsB = indsB[0]
                # end if

                if len(np.array(recent_transfers["blockNos"])[indsC][indsB]) < threshold:
                    print("less than threshold for iC,iB")
                    print("threshold: ", threshold)
                    print("len iC,iB: ", len(np.array(recent_transfers["blockNos"])[indsC][indsB]))
                    continue
                # end if

                indsCC = []
                if not collection in ["any", "all"]:
                    indsCC = np.where(np.array(recent_transfers["blueChipHoldings"]
                        [collection])[indsC][indsB] == 1)
                    if type(indsCC) == type(test_tuple):
                        indsCC = indsCC[0]
                    # end if

                    if len(list(set(np.array(recent_transfers["wallets"])[indsC][indsB][indsCC]))) < threshold:
                        print("less than threshold for iC,iB,iCC: ", collection)
                        print("threshold: ", threshold)
                        print("len iC,iB,iCC: ", len(np.array(recent_transfers["blockNos"])[indsC][indsB][indsCC]))
                        continue
                    # end if
                # end if
                print("indsCC: ", indsCC)

                indsTT = []
                if not transaction_type in ["any", "all"]:
                    if indsCC == []:
                        indsTT = np.where(np.array(recent_transfers["transfer_types"])[indsC][indsB]
                            == transaction_type)
                    else:
                        indsTT = np.where(np.array(recent_transfers["transfer_types"])[indsC][indsB][indsCC]
                            == transaction_type)
                    # end if/else
                # end if
                print("indsTT: ", indsTT)
                if indsTT != []:
                    if indsCC == []:
                        if len(np.array(recent_transfers["transfer_types"])[indsC][indsB][indsTT]) < threshold:
                            print("less than threshold for iC,iB,iCC,iTT: ", collection)
                            print("threshold: ", threshold)
                            print("len iC,iB,iCC,iTT: ", len(np.array(recent_transfers["blockNos"])[indsC][indsB][indsTT]))
                            continue
                        # end if
                    else:
                        if len(np.array(recent_transfers["transfer_types"])[indsC][indsB][indsCC][indsTT]) < threshold:
                            print("less than threshold for iC,iB,iTT: ", collection)
                            print("threshold: ", threshold)
                            print("len iC,iB,iTT: ", len(np.array(recent_transfers["blockNos"])[indsC][indsB][indsCC][indsTT]))
                            continue
                        # end if
                    # end if
                # end if

                ## next might as well see if we can get the OS stuff 
                ## b/c if not we also skip (tests if NFT vs ERC20 etc.)
                os_url = OS_BASE + contract + "/1"
                driver.get(os_url)
                html_source = driver.page_source
                try:
                    os_collection = html_source.split('CollectionLink--link" href="')[1].split('"')[0]
                except Exception as err:
                    await self.channel_log.send("warning! OS collection not found for contract: " + contract)
                    print("OS collection not found for contract: ", contract)
                    print("err 405: ", err)
                    print("err.args 406: ", err.args[:])
                    continue
                # end try/except
                os_name = html_source.split('CollectionLink--link" href="')[1].split(
                    "<div class=")[1].split(">")[1].split("<")[0]
                os_url = "https://opensea.io" + os_collection
                print("grabbed os name and url!")

                ## now we might as well grab holdings
                description = ""; nl1 = -1; nl2 = -1; nl3 = -1
                num_loops = np.array(recent_transfers["wallets"])[indsC][indsB]; nl1 = len(num_loops)
                if indsCC != []:
                    num_loops = num_loops[indsCC]; nl2 = len(num_loops)
                # end if
                if indsTT != []:
                    num_loops = num_loops[indsTT]; nl3 = len(num_loops)
                # end if
                num_loops = len(num_loops)

                holders_processed = []
                for kk in range(num_loops):
                    if indsCC == []:
                        if indsTT == []:
                            wall = np.array(recent_transfers["wallets"])[indsC][indsB][kk]
                            indsW = np.where(np.array(recent_transfers["wallets"])[indsC][indsB] == wall)
                        else:
                            wall = np.array(recent_transfers["wallets"])[indsC][indsB][indsTT][kk]
                            indsW = np.where(np.array(recent_transfers["wallets"])[indsC][indsB][indsTT] == wall)
                        # end if/else
                    else:
                        if indsTT == []:
                            wall = np.array(recent_transfers["wallets"])[indsC][indsB][indsCC][kk]
                            indsW = np.where(np.array(recent_transfers["wallets"])[indsC][indsB][indsCC] == wall)
                        else:
                            wall = np.array(recent_transfers["wallets"])[indsC][indsB][indsCC][indsTT][kk]
                            indsW = np.where(np.array(recent_transfers["wallets"])[indsC][indsB][indsCC][indsTT] == wall)
                        # end if/else
                    # end if/else
                    if type(indsW) == type(test_tuple):
                        indsW = indsW[0]
                    # end if
                    if wall in holders_processed:
                        continue
                    # end if
                    holders_processed.append(wall)

                    ## assume transfer type is any (for now)
                    if indsCC == []:
                        if indsTT == []:
                            transfers_arr = np.array(recent_transfers["transfer_types"])[indsC][indsB][indsW]
                        else:
                            transfers_arr = np.array(recent_transfers["transfer_types"])[indsC][indsB][indsTT][indsW]
                        # end if/else
                    else:
                        if indsTT == []:
                            transfers_arr = np.array(recent_transfers["transfer_types"])[indsC][indsB][indsCC][indsW]
                        else:
                            transfers_arr = np.array(recent_transfers["transfer_types"])[indsC][indsB][indsCC][indsTT][indsW]
                        # end if/else
                    # end if/else
                    num_bought = 0
                    num_sold   = 0
                    num_minted = 0
                    num_burned = 0
                    for tt in transfers_arr:
                        if tt == "bought":
                            num_bought += 1
                        elif tt == "sold":
                            num_sold += 1
                        elif tt == "minted":
                            num_minted += 1
                        elif tt == "burned":
                            num_burned += 1
                        else:
                            print("err 457, tt: ", tt)
                            raise
                        # end if/elifs/else
                    # end for
                    transfers_string = ""
                    if num_bought > 0:
                        transfers_string += str(num_bought) + " bought "
                    if num_sold > 0:
                        if transfers_string != "":
                            transfers_string += "and "
                        # end if
                        transfers_string += str(num_sold) + " sold "
                    if num_minted > 0:
                        if transfers_string != "":
                            transfers_string += "and "
                        # end if
                        transfers_string += str(num_minted) + " minted "
                    # end if
                    if num_burned > 0:
                        if transfers_string != "":
                            transfers_string += "and "
                        # end if
                        transfers_string += str(num_burned) + " burned "
                    # end if

                    blues = ""
                    for nft in self.nfts:
                        if indsCC == []:
                            if indsTT == []:
                                val = np.array(recent_transfers["blueChipHoldings"][nft])[indsC][indsB][kk]
                            else:
                                val = np.array(recent_transfers["blueChipHoldings"][nft])[indsC][indsB][indsTT][kk]
                            # end if/else
                        else:
                            if indsTT == []:
                                val = np.array(recent_transfers["blueChipHoldings"][nft])[indsC][indsB][indsCC][kk]
                            else:
                                val = np.array(recent_transfers["blueChipHoldings"][nft])[indsC][indsB][indsCC][indsTT][kk]
                            # end if/else
                        # end if/else

                        if val:
                            blues += nft + "/"
                        # end if
                    # end for
                    blues = blues[:-1]
                    description += transfers_string + " by a " + blues + " holder, "
                # end for kk
                if description == "":
                    print("num_loops: ", num_loops)
                    print("nl1: ", [nl1])
                    print("nl2: ", [nl2])
                    print("nl3: ", [nl3])
                    print("indsTT: ", indsTT)
                    raise

                description = description[:-2] + "."
                if len(description) > 1000:
                    description = ", ".join(description[:1000].split(", ")[:-1]) + "..."
                # end if
                print("done looping over blues!")

                alert_description = ">= " + str(int(threshold))
                if   "any"    in transaction_type:
                    alert_description += " Transfers by "
                elif "minted" in transaction_type:
                    alert_description += " Mints by "
                elif "bought" in transaction_type:
                    alert_description += " Buys by "
                elif "sold"   in transaction_type:
                    alert_description += " Sells by "
                elif "burned"   in transaction_type:
                    alert_description += " Burns by "
                # end if/elif
                
                if collection in ["any", "all"]:
                    alert_description += "any of the tracked blue chip holders "
                else:
                    alert_description += collection + " holders "
                # end if/else
                alert_description += (" in the last %.1f minutes." % (num_blocks*15/60.0))

                ## now go ahead and send the alert!
                embed = discord.Embed(title = os_name, description = alert_description)
                embed.set_footer(text = "Built for NFT Round Table, Powered by @TheLunaLabs",
                    icon_url = self.ICON_URL)
                embed.set_thumbnail(url = self.ICON_URL)
                embed.add_field(name = "OpenSea", value = os_url, inline=False)
                embed.add_field(name = "Contract Address", value = 
                    "https://etherscan.io/token/" + contract, inline=False)
                embed.add_field(name = "Blue Chips Tracked", value = ", ".join(list(self.nfts.keys())),
                    inline=False)
                embed.add_field(name = "Alert Details", value=description,
                    inline=False)
                wembedCnt = 0
                while wembedCnt < 10:
                  try:
                    await self.channel_msg.send(embed=embed)
                    print("sent embed!")
                    break
                  except Exception as err:
                    print("526 err: ", err)
                    print("527 err args: ", err.args[:])
                    print("sleeping for a bit")
                    await aysncio.sleep(self.LS)
                    wembedCnt += 1
                  # end try/except
                # end while
                if wembedCnt >= 10:
                  print("tried sending embed 10 times, gonna crash now")
                  raise
                # end if
            # end for jj in settings
        # end for contracts
    # end process_recent_transfers

    async def loop_forever(self):
        print("begin loop_forever")
        await self.load_holder_data()

        wcnt = 0
        block = -1
        while True:
            wcnt += 1
            print("wcnt: ", wcnt)

            try:
              block_new = self.w3.eth.get_block_number()
            except Exception as err:
              print("693 err: ", err)
              print("694 err.args: ", err.args[:])
              await asyncio.sleep(self.LS)
              continue
            # end try/except
            if block_new == block:
                await asyncio.sleep(self.LS)
                continue
            # end if
            block = block_new
            print("block: ", block)

            await self.get_settings()
            num_blocks = max(self.settings["num_blocks"])
            old_block = block - int(num_blocks)
            await self.get_transfer_data(str(old_block), str(block))

            await self.process_transfer_data()
        # end while True
    # end loop_forever

    def discord_bot(self):
        client = discord.Client(intents=None)

        @client.event
        async def on_ready():
            self.channel_log = client.get_channel(self.CID_LOG)
            self.channel_msg = client.get_channel(self.CID_MSG)

            await self.loop_forever()
        # end on_ready

        client.run(os.environ.get("taBotPass"))
    # end discord_bot
# end TransferAlerts

if __name__ == "__main__":
    ta = TransferAlerts()
    ta.discord_bot()
# end if
## end transfer_alerts.py
