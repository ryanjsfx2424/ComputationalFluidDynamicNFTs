import os
import json
import time
import socket
import asyncio
from web3 import Web3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class Tribulator(object):
    def __init__(self):
        print("BEGIN __init__ class Tribulator")

        self.vn = "12"
        self.CONTRACT_ADDRESS1 = "0xE740677D16705E5949c48b4c55aE22D2fE545811"
        self.CONTRACT_ADDRESST = "0x177547ef0676CDba4b9AF2617dB80BA6E04D4F8D"
        self.TRIB_ADDRESS      = "0x879d3D3a5720b9fd575f6d07A6396B1FE78C850a"
        self.DEPLOYER_ADDRESS  = "0xC7d7Cc95DeD3B8C81f17AF0e65DEf2d4abB366f7"

        self.path_abi1 = "contract/rc" + self.vn + "_abi.json"
        self.path_abiT = "contract/rc" + self.vn + "t_abi.json"
        self.os_url = "https://testnets.opensea.io/collection/rc" + self.vn + \
                      "n/activity?search[isSingleCollection]=true&search"   + \
                      "[eventTypes][0]=AUCTION_CREATED&search[eventTypes][1]=AUCTION_SUCCESSFUL"

        self.WEI_PER_ETH = 1e18

        self.QS = 0.01
        self.MS = 6.01
        self.LS = 3.1

        self.load_deployer()
        self.load_abi()
        self.init_w3()
        self.init_contract()
        self.init_webscraper()

        self.trib_counter = 0

        print("SUCCESS __init__ class Tribulator")
    # end __init__

    def load_deployer(self):
        self.deployer = ""
        with open("git_ignores_me.mp4", "r") as fid:
            for line in fid:
                self.deployer += line.replace("\n","")
            # end for
        # end with
    # end load_deployer

    def load_abi(self):
        print("BEGIN load_abi class Tribulator")

        with open(self.path_abi1, "r") as fid:
            rl = "".join(fid.readlines())
            self.abi1 = json.loads(rl)
        # end with
        with open(self.path_abiT, "r") as fid:
            rl = "".join(fid.readlines())
            self.abiT = json.loads(rl)
        # end with

        print("SUCCESS load_abi class Tribulator")
    # end load_abi

    def init_w3(self):
        print("BEGIN init_w3 class Tribulator")

        self.w3 = Web3(Web3.HTTPProvider(os.environ["INFURA_RINK"]))
        from web3.middleware import geth_poa_middleware # needed for rinkeby
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        print("BEGIN init_w3 class Tribulator")
    # end init_w3

    def init_contract(self):
        print("BEGIN init_contract class Tribulator")

        self.contract = self.w3.eth.contract(address=self.CONTRACT_ADDRESS1, abi=self.abi1)
        totalSupply = self.contract.functions.totalSupply().call()
        print("totalSupply1: ", totalSupply) # checks w3 connection

        self.contractT = self.w3.eth.contract(address=self.CONTRACT_ADDRESST, abi=self.abiT)
        totalSupply = self.contractT.functions.totalSupply().call()
        print("totalSupplyT: ", totalSupply) # checks w3 connection

        print("SUCCESS init_contract class Tribulator")
    # end init_contract

    def init_webscraper(self):
        print("BEGIN init_webscraper class Tribulator")

        self.options = Options()
        self.options.headless = True
        #self.options.headless = False

        self.exec_path = "/root/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver_linux"
        if socket.gethostname() == "MB-145.local":
            self.exec_path = "/Users/ryanjsfx/Documents/ComputationalFluidDynamicNFTs/V3.0.4/TransferAlerts/geckodriver"
        # end if

        print("SUCCESS init_webscraper class Tribulator")
    # end init_webscraper

    def tribulation(self, tokenIds):
        print("BEGIN tribulation class Tribulator")

        ## step 1, get wallets of tokenIds to be tribulated
        prevOwners = []
        for tokenId in tokenIds:
            prevOwners.append(self.contract.functions.ownerOf(tokenId).call())
        # end for

        #'''
        ## step 2, tribulate tokenIds that were listed below mint
        transaction = self.contract.functions.tribulation(tokenIds).buildTransaction({"from":self.TRIB_ADDRESS})
        gas_estimate = self.w3.eth.estimateGas(transaction)

        transaction.update({ "gas": int(1.2*gas_estimate) })
        transaction.update({ "nonce": self.w3.eth.get_transaction_count(self.TRIB_ADDRESS) })
        signed_tx = self.w3.eth.account.sign_transaction(transaction, os.environ["TRIB"])
        print("tribulation signed_tx: ")#, signed_tx)

        txn_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print("tribulation txn_hash: ")#, txn_hash)
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        print("tribulation txn_receipt: ")#, txn_receipt)
        #'''

        ## step 3, send them a consolation nft
        for prevOwner in prevOwners:
            transaction = self.contractT.functions.safeTransferFrom(
                self.DEPLOYER_ADDRESS, prevOwner, self.trib_counter).buildTransaction(
                {"from":self.DEPLOYER_ADDRESS})

            gas_estimate = self.w3.eth.estimateGas(transaction)
            self.trib_counter += 1

            transaction.update({ "gas": int(1.2*gas_estimate) })
            transaction.update({ "nonce": self.w3.eth.get_transaction_count(self.DEPLOYER_ADDRESS) })
            signed_tx = self.w3.eth.account.sign_transaction(transaction, self.deployer)
            print("safeTransferFrom signed_tx: ")#, signed_tx)

            txn_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print("safeTransferFrom txn_hash: ")#, txn_hash)
            txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
            print("safeTransferFrom txn_receipt: ")#, txn_receipt)
        # end for prevOwners

        print("SUCCESS tribulation class Tribulator")
    # end tribulation

    def get_mint_price(self):
        print("BEGIN get_mint_price")

        sale_state = self.contract.functions.sale_state().call()
        print("sale_state: ", sale_state)
        if sale_state == 2:
            self.mint_price = self.contract.functions.public_sale_cost().call() / self.WEI_PER_ETH
            print("public sale mint_price: ", self.mint_price)

        elif sale_state == 1:
            self.mint_price = self.contract.functions.pre_sale_cost().call() / self.WEI_PER_ETH
            print("pre sale mint_price: ", self.mint_price)
        else:
            print("sale is closed")
            self.mint_price = -1
            return
        # end if/elif/else

        print("SUCCESS get_mint_price")
    # end get_mint_price

    async def scrape_os(self):
        print("BEGIN scrape_os class Tribulator")

        while True:
            await asyncio.sleep(self.QS) # long sleep later

            # first check the mint price (changes pre to public sales)
            self.get_mint_price()
            if self.mint_price <= 0:
                print("mint price <= 0 so not scraping this time. Sleeping one min")
                await asyncio.sleep(self.LS)
                continue
            # end if

            ## check listings, if below mint price, tribulation tokenId
            driver = webdriver.Firefox(options=self.options, 
                               executable_path=self.exec_path)

            try:
                driver.get(self.os_url)
            except Exception as err:
                print("130 err: ", err)
                print("131 err.args: ", err.args[:])
                driver.close()

                print("closed driver, doing a long sleep before new loop")
                await asyncio.sleep(self.LS)
                continue
            # end try/except

            html = driver.page_source
            with open("os_html.txt", "w") as fid:
                fid.write(html)
            # end with open

            await asyncio.sleep(self.MS)
            price_elems = driver.find_elements(By.CSS_SELECTOR, "div.Price--amount")
            print("price_elems: ", price_elems)
            print("len price_elems: ", len(price_elems))

            name_elems = driver.find_elements(By.CSS_SELECTOR, "div.sc-7qr9y8-0.kKWQrL")
            print("name_elems: ", name_elems)
            print("len_name_elems: ", len(name_elems))

            event_elems = driver.find_elements(By.CSS_SELECTOR, "h6.sc-1xf18x6-0.sc-1aqfqq9-0.evlrPY.cSiicL")
            driver.quit()
            print("event_elems: ", event_elems)
            print("len event_elems: ", len(event_elems))

            if len(price_elems) != len(name_elems) != len(event_elems):
                print("lens price_elems != name_elems != len(event_elems")
                sys.exit()

            elif len(price_elems) == 0:
                print("no price_elems, continuing after a long sleep")
                self.tribulation([300,302])
                sys.exit()
                await asyncio.sleep(self.LS)
                continue
            # end if/elif

            names    = []
            listings = []
            for ii in range(len(event_elems)):
                print("ii, event, name: ", ii, event_elems[ii].text, name_elems[ii].text)

                event = event_elems[ii].text
                name  = name_elems[ii].text
                if event == "Sale" and name in names:
                    ind = names.index(name)
                    del names[ind]
                    del listings[ind]
                elif event == "List":
                    names.append(name)
                    listings.append(float(price_elems[ii].text.replace(",", ".")))
                # end if/else
            # end for ii
            print("names: ", names)
            print("listings: ", listings)

            tokenIds = []
            for ii in range(len(listings)):
                print("248 ii: ", ii)
                if listings[ii] < self.mint_price:

                    tokenId = int(names[ii].split("#")[1].replace(" ","").replace("\n",""))
                    print("227 tokenId: ", tokenId)

                    owner = self.contract.functions.ownerOf(tokenId).call()
                    print("owner: ", owner)
                    print("deplo: ", self.DEPLOYER_ADDRESS)

                    if owner == self.DEPLOYER_ADDRESS:
                        print("230 token already owned by the deployer! continuing")
                        continue
                    # end if

                    tokenIds.append(tokenId)
                    print("246 tokenIds after append: ", tokenIds)
                # end if
            # end for

            if len(tokenIds) != 0:
                self.tribulation(tokenIds)
            # end if

            print("239 long sleep before new loop")
            await asyncio.sleep(self.LS)
        # end while

        print("SUCCESS scrape_os class Tribulator")
    # end scrape_os
# end Tribulator

if __name__ == "__main__":
    trib = Tribulator()
    asyncio.run(trib.scrape_os())
# end tribulation.py
