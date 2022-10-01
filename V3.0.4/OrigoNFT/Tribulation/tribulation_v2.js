import { Network, OpenSeaStreamClient } from "@opensea/stream-js";
import { WebSocket } from "ws";
import Provider from "@truffle/hdwallet-provider";
import Web3 from "web3";
import fs from "fs";
import Tx from "ethereumjs-tx";

const OS_SLUG = "rc14n";
const CONTRACT_ADDRESS  = "0xa1e04354929992b9eec85ca8269c91a089244215";
const CONTRACT_ADDRESST = "0xBeD9d7746A5def293dbA90098352c7552c93425C";
const TRIB_ADDRESS      = "0x879d3D3a5720b9fd575f6d07A6396B1FE78C850a";
const DEPLOYER_ADDRESS  = "0xC7d7Cc95DeD3B8C81f17AF0e65DEf2d4abB366f7";


const WEI_PER_ETH = 1e18;

const provider = new Provider([process.env.TRIB,
    process.env.gim1 + process.env.gim2 + process.env.gim3], process.env.INFURA_RINK);
const web3 = new Web3(provider);
const contractABI  = JSON.parse(fs.readFileSync("./abi.json",  "utf8"));
const SmartContract  = new web3.eth.Contract(contractABI, CONTRACT_ADDRESS );
const SmartContractT = new web3.eth.Contract(contractABI, CONTRACT_ADDRESST);
var trib_counter = 10;

async function tribulate(tokenIds) {
    console.log("tribulating for tokenIds: ", tokenIds);

    let prevOwners = [];
    for (var ii = 0; ii < tokenIds.length; ii++) {
        console.log("50 ii: ", ii);
        let prevOwner;
        try {
            prevOwner = await SmartContract.methods.ownerOf(tokenIds[ii]).call()
        } catch (err) {
            console.log("54 trib err: ", err)
            return {
                success: false,
                message: "Didn't get prevOwner"
            }
        }
        prevOwners.push(prevOwner);
    }
    console.log("64 got prevOwners! ", prevOwners);

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

    for (var ii = 0; ii < tokenIds.length; ii++) {
        console.log("71 ii: ", ii);
        try {
            const receipt = await SmartContractT.methods.safeTransferFrom(
                DEPLOYER_ADDRESS, prevOwners[ii], trib_counter
            ).send({
                from: DEPLOYER_ADDRESS
            });
            
            console.log("120 receipt txHas: ", receipt.transactionHash);
        } catch (err) {
            console.log("121 trib err; ", err)
            return {
                success: false,
                message: "Didn't transfer a consolation nft"
            }
        }
    }
    console.log("129 trib");
}

const client = new OpenSeaStreamClient({
    token: process.env.rtOS,
    network: Network.TESTNET, // default is Network.MAINNET
    connectOptions: {
        transport: WebSocket
    }
});

client.connect();

client.onItemListed(OS_SLUG, async(event) => {
    if (Number(event.payload.base_price) < 0.089*WEI_PER_ETH) {
        const tokenId = Number(event.payload.item.nft_id.split("/").pop());
        console.log("97 tokenId pop'd: ", tokenId);
        await tribulate([tokenId]);
        console.log("after trib");
    } 
});
