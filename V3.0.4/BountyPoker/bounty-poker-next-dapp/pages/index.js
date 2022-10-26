import { useState, useEffect } from 'react'
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import contractABI from '../public/contractABI.json'
import Web3 from 'web3'
import Web3EthContract from 'web3-eth-contract'

const CONTRACT_ADDRESS = "0x457b4a79785FE1a17DA79b995248e00940b8C639"
const CHAIN_ID = 5
const CHAIN_NAME = "GOERLI"
const WEI_PER_ETH = 1e18

// console.log("contractABI: ", contractABI)
console.log("CONTRACT_ADDRESS: ", CONTRACT_ADDRESS)

export default function Home() {
    const [isWalletConnected, setIsWalletConnected] = useState(false);
    const [walletAddress, setWalletAddress] = useState("");
    const [isCorrectChain, setIsCorrectChain] = useState(false);
    const [isButtonDisabled, setIsButtonDisabled] = useState(false);
    const [buyInCost, setBuyInCost] = useState(0.05)
    const [walletBalance, setWalletBalance] = useState(0)

  // I should change this to 'deposit'
  const buyIn = async() => {
      setIsButtonDisabled(true)
      
      const SmartContractObj = fetchSmartContractObj();

      let gasLimitEstimate;
      try {
          gasLimitEstimate = await SmartContractObj.methods.buyIn().estimateGas({
              from: window.ethereum.selectedAddress,
              value: String(buyInCost*WEI_PER_ETH),
          })
      } catch (err) {
          console.log("37 mint err: ", err);
          alert("😥 Something went wrong estimate gas");
      }
      console.log("got gasLimitEstimate! ", gasLimitEstimate);
      console.log({
        gasLimitEstimate: gasLimitEstimate,
      });

      let web3 = new Web3(window.ethereum);
      let gasPriceEstimate = await web3.eth.getGasPrice();

      console.log({resultOfGasPriceEstimate: gasPriceEstimate});

      try {
          const receipt = await SmartContractObj.methods.buyIn().send({
              gasLimit: String(Math.round(1.2 * gasLimitEstimate)),
              gasPrice: String(Math.round(1.1 * gasPriceEstimate)),
              to: CONTRACT_ADDRESS,
              from: window.ethereum.selectedAddress,
              value: String(buyInCost*WEI_PER_ETH)});
          console.log("293 mint receipt: ", receipt);
          console.log({
              success: true,
              status: receipt,
              status2: "SUCCESS",
          })
      }
      catch (err) {
          console.log("65 buyIn err", err);
          alert("Something went wrong when trying to buyIn");
      }
      setIsButtonDisabled(false);
	}

  function fetchSmartContractObj() {
      Web3EthContract.setProvider(window.ethereum);
      let web3 = new Web3(window.ethereum);
      const SmartContractObj = new Web3EthContract(contractABI, CONTRACT_ADDRESS);
      return SmartContractObj;
  }

  const fetchBuyInCost = async() => {
      const SmartContractObj = fetchSmartContractObj();
      
      try {
          let cost = await SmartContractObj.methods.cost().call();
          cost /= WEI_PER_ETH;
          console.log("cost: ", cost)
          setBuyInCost(cost);
      } catch {
          console.log("error getting cost");
          alert("😥 Something went wrong fetching buy in cost")
      }
  }

  const fetchBalance = async() => {
    const SmartContractObj = fetchSmartContractObj();
    
    try {
        let balance = await SmartContractObj.methods.balance(window.ethereum.selectedAddress).call();
        balance /= WEI_PER_ETH;
        console.log("balance: ", balance)
        setWalletBalance(balance);
    } catch {
        console.log("error getting cost");
        alert("😥 Something went wrong fetching balance")
    }
}

	//CONNECT WALLET
	function walletListener() {
		  if (window.ethereum) {
			    window.ethereum.on("accountsChanged", (account) => {
			
              if (account.length > 0) {
				          setWalletAddress(account[0])
				          setIsWalletConnected(true)
				          console.log("30 wallet is connected");
			        } else {
				          setIsWalletConnected(false)
				          alert("install metamask extension!!");
			        }
			    });
			
          window.ethereum.on("chainChanged", (chainId) => {
				      if (Number(chainId) === CHAIN_ID) {
					        setIsCorrectChain(true);
                  fetchBuyInCost()
                  fetchBalance()
				      } else {
					        setIsCorrectChain(false);
					        alert("Change chain to " + CHAIN_NAME);
				      }
			    })
		  } else {
			    alert("install metamask extension!!");
		  }
	}

	useEffect(() => {
      connectWallet()
  }, [])
	
  const connectWallet = async () => {
	    if (window.ethereum) {
		      console.log("has window ethereum");

          var account;
          try {
              account = await window.ethereum.request({method: 'eth_accounts'})
              console.log("got account: ", account)
          } catch {
              console.log("error grabbing account");
              account = "";
          }

          if (account.length > 0) {
              var chainId;
              try {
                  chainId = await window.ethereum.request({method: 'net_version'})
              } catch {
                  console.log("error grabbing account");
                  chainId = -1;
              }

              setWalletAddress(account[0])
              setIsWalletConnected(true)

              if (Number(chainId) === CHAIN_ID) {
                  setIsCorrectChain(true)
                  fetchBuyInCost()
                  fetchBalance()
              } else {
                  setIsCorrectChain(false)
                  alert("Change chain to " + CHAIN_NAME);
              }
          } else {
              setIsWalletConnected(false)
              setIsCorrectChain(false)
              alert("Could not get account - have you logged into metamask?")
          }
	    } else {
		      alert("install metamask extension!!");
	    }
	};

  return (
    <div className={styles.container}>
      <Head>
        <title>Bounty Poker</title>
        <meta name="description" content="Bounty Poker Slogan" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
            Welcome to <a href="https://twitter.com/bountypokernft">Bounty Poker!</a>
        </h1>

        <h2 className={styles.title}>
            Buy in cost is {buyInCost} eth.
        </h2>

        {
          (isWalletConnected) ?
            <>
                <button 
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
                    onClick={buyIn}
                    disabled={isButtonDisabled}
                >Buy In</button>

                <h2 className={styles.title}>
                    Your current balance: {walletBalance} eth.
                </h2>
            </>
          :
              <button 
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
                onClick={connectWallet}
                disabled={isButtonDisabled}
              >Connect Wallet</button>
        }
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}
