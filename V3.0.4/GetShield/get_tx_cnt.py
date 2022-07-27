import os
import ast

contractAddress = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D" # bayc
contractAddress = "0xDb3B2e1F699CaF230eE75bfBE7d97d70F81bC945" #dormantDragons
contractAddress = "0x7305c03F5b449dA4Bdc47fbaaB3eb8510493132C" # knightsWTF
ETHERSCAN_URL = "https://api.etherscan.io/api"
ETHERSCAN_KEY = os.environ.get("ETHERSCAN_API_KEY")
print("ETHERSCAN_KEY: ", ETHERSCAN_KEY)
url = ETHERSCAN_URL + "?module=proxy&action=eth_getTransactionCount&address="
url += contractAddress + "&tag=latest&apikey=" + ETHERSCAN_KEY

url = ETHERSCAN_URL + "?module=account&action=txlist&address="
url += contractAddress
url += "&startblock=0&endblock=99999999&page=1&sort=asc&apikey"
url += ETHERSCAN_KEY


command = "curl --request GET --url '" + url + "' > log4.txt"
print("command: ", command)
os.system(command)

with open("log.txt", "r") as fid:
  line = fid.read()
# end with open

line = ast.literal_eval(line)
print("line.keys: ", line.keys())
print("len result: ", len(line["result"]))
print("line[result][0].keys: ", line["result"][0].keys())
print(line["result"][0]["confirmations"])
print(line["result"][1]["confirmations"])
print(line["result"][-1]["confirmations"])
print(line["result"][5]["confirmations"])
