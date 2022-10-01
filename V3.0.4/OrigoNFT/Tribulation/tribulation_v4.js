import { Network, OpenSeaStreamClient } from "@opensea/stream-js";
import { WebSocket } from "ws";
import Provider from "@truffle/hdwallet-provider";
import Web3 from "web3";
import fs from "fs";
import Tx from "ethereumjs-tx";

const OS_SLUG = "origogenesis";
const CONTRACT_ADDRESS  = "0x4485c283D597e672497Cf0a298dadF9E118B1E18";
const TRIB_ADDRESS      = "0x585bf720Bd3eDA4245205b5f38dA31836125e2ec";
const DEPLOYER_ADDRESS  = "0x89C2E9066e34A62814B6F6c47DCaCb8c0F1f6aAd";


const WEI_PER_ETH = 1e18;

const provider = new Provider([process.env.TRIB1 + process.env.TRIB2,
    process.env.gim1 + process.env.gim2 + process.env.gim3], process.env.INFURA_MAIN);
const web3 = new Web3(provider);
const contractABI  = JSON.parse(fs.readFileSync("./abi-origo-genesis.json",  "utf8"));
const SmartContract  = new web3.eth.Contract(contractABI, CONTRACT_ADDRESS );
var trib_counter = 10;

async function tribulate(tokenIds) {
    console.log("tribulating for tokenIds: ", tokenIds);

    try {
        const receipt = await SmartContract.methods.tribulation(tokenIds).send({ from: TRIB_ADDRESS });
        console.log("100 trib receipt txHash", receipt.transactionHash);

    } catch (err) {
        console.log("58 tribulate err: ", err);
        return {
            success: false,
            message: "Didn't tribulate successfully"
        }
    }
}

const client = new OpenSeaStreamClient({
    token: process.env.rtOS,
    connectOptions: {
        transport: WebSocket
    }
});

client.connect();

client.onItemListed(OS_SLUG, async(event) => {
    if (Number(event.payload.base_price) < 0.1*WEI_PER_ETH) {
        console.log("50 event: ", event)
        console.log("51 event.payload: ", event.payload)
        console.log("52 event.payload.item: ", event.payload.item)
        console.log("52 event.payload.item.nft_id: ", event.payload.item.nft_id)
        const tokenId = Number(event.payload.item.nft_id.split("/").pop());
        console.log("97 tokenId pop'd: ", tokenId);
        await tribulate([tokenId]);
        console.log("after trib");
    } 
});
