// constants
import Web3EthContract from "web3-eth-contract";
import Web3 from "web3";
// log
import { fetchData } from "../data/dataActions";
import { Web3Provider } from "@ethersproject/providers";

import React from 'react';
import WalletLink from "walletlink";

const connectRequest = () => {
  return {
    type: "CONNECTION_REQUEST",
  };
};

const connectSuccess = (payload) => {
  return {
    type: "CONNECTION_SUCCESS",
    payload: payload,
  };
};

const connectFailed = (payload) => {
  return {
    type: "CONNECTION_FAILED",
    payload: payload,
  };
};

const updateAccountRequest = (payload) => {
  return {
    type: "UPDATE_ACCOUNT",
    payload: payload,
  };
};

export const connect = () => {
  return async (dispatch) => {
    dispatch(connectRequest());
    const abiResponse = await fetch("config/abi.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const abi = await abiResponse.json();

    const abiWethResponse = await fetch("config/abiWeth.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const abiWeth = await abiWethResponse.json();

    const configResponse = await fetch("config/config.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const CONFIG = await configResponse.json();
    const { ethereum } = window;
    const metamaskIsInstalled = ethereum && ethereum.isMetaMask;
    if (metamaskIsInstalled) {
      Web3EthContract.setProvider(ethereum);
      let web3 = new Web3(ethereum);
      try {
        const accounts = await ethereum.request({
          method: "eth_requestAccounts",
        });
        const networkId = await ethereum.request({
          method: "net_version",
        });
        if (networkId == CONFIG.NETWORK.ID) {
          const SmartContractObj = new Web3EthContract(
            abi,
            CONFIG.CONTRACT_ADDRESS
          );
          const SmartContractObjWeth = new Web3EthContract(
            abiWeth,
            CONFIG.CONTRACT_ADDRESS_WETH
          );
          dispatch(
            connectSuccess({
              account: accounts[0],
              smartContract: SmartContractObj,
              smartContractWeth: SmartContractObjWeth,
              web3: web3,
            })
          );
          // Add listeners start
          ethereum.on("accountsChanged", (accounts) => {
            dispatch(updateAccount(accounts[0]));
          });
          ethereum.on("chainChanged", () => {
            window.location.reload();
          });
          // Add listeners end
        } else {
          dispatch(connectFailed(`Change network to ${CONFIG.NETWORK.NAME}.`));
        }
      } catch (err) {
        dispatch(connectFailed("Something went wrong."));
      }
    } else {
      dispatch(connectFailed("Install Metamask, or click the Connect Coinbase Wallet Button."));
    }
  };
};

export const connectCoinbase = () => {
  return async (dispatch) => {
    dispatch(connectRequest());
    const abiResponse = await fetch("config/abi.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const abi = await abiResponse.json();

    const abiWethResponse = await fetch("config/abiWeth.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const abiWeth = await abiWethResponse.json();

    const configResponse = await fetch("config/config.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const CONFIG = await configResponse.json();
    const { ethereum } = window;
    try {
      // Initialize Walletlink
      const walletLink = new WalletLink({
        appName: 'demo-app',
        darkMode: true
      });
      console.log("Instantiated WalletLink object");

      const provider = walletLink.makeWeb3Provider('https://rinkeby.infura.io/v3/55d040fb60064deaa7acc8e320d99bd4', 4);
      //setWalletlinkProvider(provider);
      const accounts = await provider.request({
        method: 'eth_requestAccounts'
      });
      const networkId = await ethereum.request({
        method: "net_version",
      });
      console.log("requested accounts");
      if (networkId == CONFIG.NETWORK.ID) {
        console.log("connected to correct network (good)");
        const SmartContractObj = new Web3EthContract(
          abi,
          CONFIG.CONTRACT_ADDRESS
        );
        const SmartContractObjWeth = new Web3EthContract(
          abiWeth,
          CONFIG.CONTRACT_ADDRESS_WETH
        );
        console.log("Instantiated Web3EthContract object");
        dispatch(
          connectSuccess({
            account: accounts[0],
            smartContract: SmartContractObj,
            smartContractWeth: SmartContractObjWeth,
            web3: web3,
          })
        );
      // Add listeners start
      ethereum.on("accountsChanged", (accounts) => {
        console.log("changing accounts");
        dispatch(updateAccount(accounts[0]));
      });
      ethereum.on("chainChanged", () => {
        console.log("changed chain so reloading");
        window.location.reload();
      });
    // Add listeners end
    } else {
      dispatch(connectFailed(`Change network to ${CONFIG.NETWORK.NAME}.`));
    }
    } catch (err) {
        console.log(err);
        dispatch(connectFailed("Something went wrong."));
    }
  };
};

export const updateAccount = (account) => {
  return async (dispatch) => {
    dispatch(updateAccountRequest({ account: account }));
    dispatch(fetchData(account));
  };
};
