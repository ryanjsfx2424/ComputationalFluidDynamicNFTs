import React, { useEffect, useState, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ethers } from "ethers";
import keccak256 from "keccak256";
import MerkleTree from "merkletreejs";
import { connect } from "./redux/blockchain/blockchainActions";
import { fetchData } from "./redux/data/dataActions";
import * as s from "./styles/globalStyles";
import styled from "styled-components";
import FadeIn from "react-fade-in";
import "./styles/styles.css";
require('dotenv').config();
const whitelist = require('./whitelisted_addresses.json');

const disconnectCoinbase = () => {
  walletlinkProvider.close();
  setWalletlinkProvider(null);
};

const truncate = (input, len) =>
  input.length > len ? `${input.substring(0, len)}...` : input;

export const StyledButton = styled.button`
  padding: 10px;
  border-radius: 50px;
  border: none;
  background-color: var(--secondary);
  padding: 10px;
  font-weight: bold;
  color: var(--secondary-text);
  width: 100px;
  cursor: pointer;
  box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  -webkit-box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  -moz-box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }
`;

export const StyledButtonBusy = styled.button`
  padding: 10px;
  border-radius: 50px;
  border: none;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }
  background-image: url(config/images/SiteBoxCnTConscrip.png);
  background-repeat: no-repeat;
  background-size: 100%;
  height: 100px;
  width: 200px;
  background-color: transparent;
`;

export const StyledButtonMint = styled.button`
  padding: 10px;
  border-radius: 50px;
  border: none;
  padding: 10px;
  font-weight: bold;
  cursor: pointer;
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }
  background-image: url(config/images/ButtonHead-Standard-Mint.svg);
  background-repeat: no-repeat;
  background-size: 100%;
  height: 100px;
  width: 200px;
  background-color: transparent;
`;

export const StyledRoundButton = styled.button`
  padding: 10px;
  border-radius: 100%;
  border: none;
  background-color: var(--primary);
  padding: 10px;
  font-weight: bold;
  font-size: 15px;
  color: var(--primary-text);
  width: 30px;
  height: 30px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 4px 0px -2px rgba(250, 250, 250, 0.3);
  -webkit-box-shadow: 0px 4px 0px -2px rgba(250, 250, 250, 0.3);
  -moz-box-shadow: 0px 4px 0px -2px rgba(250, 250, 250, 0.3);
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }
`;

export const ResponsiveWrapper = styled.div`
  margin-top: auto !important;
  margin-bottom: auto !important;
  }
`;

export const StyledBox = styled.img`
  display: block;
  z-index: 200;
  width: 50%;
  background-position: center;
  margin-left: auto !important;
  margin-right: auto !important;
  top: 50%;
  transform: translate(0, 25%);
`;

export const StyledOrigo = styled.img`
  position: absolute;
  z-index: 200;
  left: 0%;
  top: 0%;
  background: transparent;
  margin-top: 0;
  margin-left: 0;
  width: 60vw;
`;

export const StyledTwitter = styled.img`
  position: absolute;
  z-index: 200;
  right: 6%;
  top: 0%;
  background: transparent;
  width: 8%;
`;

export const StyledDiscord = styled.img`
  position: absolute;
  z-index: 200;
  right: 11%;
  top: 0%;
  background: transparent;
  width: 8%;
`;

export const StyledOpensea = styled.img`
  position: absolute;
  z-index: 200;
  right: 1%;
  top: 0%;
  background: transparent;
  width: 8%;
`;

export const StyledWalletFeedback = styled.img`
  cursor: pointer,
  marginLeft: 5%,
  marginTop: 29.3%,
  position: absolute,
  display: flex,
  zIndex: 5003,
  maxWidth: 38%,
  height: auto,
`;

export const MyStyledButton = styled.button`
  cursor: pointer;
  box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  -webkit-box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  -moz-box-shadow: 0px 6px 0px -2px rgba(250, 250, 250, 0.3);
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }
`;

export const StyledButtonConnect = styled.button`
  cursor: pointer;
  :active {
    box-shadow: none;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
  }

  display: flex;
  position: absolute;
  z-index: 5001;
  max-width: 75%;
  height: auto;
`;

export const StyledScroll = styled.img`
  position: absolute;
  z-index: 200;
  right: 3%;
  top: 10%;
  background: transparent;
  width: 35%;
`;

export const StyledMintButton = styled.img`
  width: 200px;
  @media (min-width: 767px) {
    width: 300px;
  }
  transition: width 0.5s;
  transition: height 0.5s;
`;

export const StyledLink = styled.a`
  color: var(--secondary);
  text-decoration: none;
  font-size: 32px;
`;

function hashAccount(userAddress) {
  return Buffer.from(ethers.utils.solidityKeccak256(['address'], [userAddress]).slice(2), 'hex');
}
function generateMerkleTree(addresses) {
  const merkleTree = new MerkleTree(
    addresses.map(hashAccount), keccak256, { sortPairs: true }
  );
  return merkleTree;
}
function generateMerkleProof(userAddress, addresses) {
  const merkleTree = generateMerkleTree(addresses);
  const proof = merkleTree.getHexProof(hashAccount(userAddress));
  return proof;
}

function App() {
  const dispatch = useDispatch();
  const blockchain = useSelector((state) => state.blockchain);
  const data = useSelector((state) => state.data);
  const [mintingNft, setMintingNft] = useState(false);
  const [feedback, setFeedback] = useState(``);
  const [walletState, setWalletState] = useState(`CONNECT WALLET`);
  const [gasText1, setGasText1] = useState(`Mint price is subject`);
  const [gasText2, setGasText2] = useState(`to GAS fees`);
  const [pricePer1, setPricePer1] = useState(`Price Per Relic`);
  const [totalTextLeft, setTotalTextLeft] = useState(`Total`);
  const [headerText, setHeaderText] = useState(`Origo Whitelist Sale`);
  const [mintLimitText, setMintLimitText] = useState(`2 Per Wallet`);
  const [pricePer2, setPricePer2] = useState(`0.089 - ETH`);
  const [saleState, setSaleState] = useState(1);
  const [mintLimitPerPhase, setMintLimitPerPhase] = useState(2);
  const [saleStateText, setSaleStateText] = useState(`WL Sale`);
  const [totalTextRight, setTotalTextRight] = useState(`0.089 - ETH`);
  const [mintCost, setMintCost] = useState(0.089);
  // const [headerText, setHeaderText] = useState(`Origo Public Sale`);
  // const [mintLimitText, setMintLimitText] = useState(`3 Per Wallet`);
  // const [pricePer2, setPricePer2] = useState(`0.099 - ETH`);
  // const [saleState, setSaleState] = useState(2);
  // const [mintLimitPerPhase, setMintLimitPerPhase] = useState(3);
  // const [saleStateText, setSaleStateText] = useState(`Public Sale`);
  // const [totalTextRight, setTotalTextRight] = useState(`0.099 - ETH`);
  // const [mintCost, setMintCost] = useState(0.099);
  const [mintAmount, setMintAmount] = useState(1);
  const [numMinted, setNumMinted] = useState(0);
  const [success, setSuccess] = useState(0);
  const [CONFIG, SET_CONFIG] = useState({
    CONTRACT_ADDRESS: "",
    SCAN_LINK: "",
    NETWORK: {
      NAME: "",
      SYMBOL: "",
      ID: 0,
    },
    NFT_NAME: "",
    SYMBOL: "",
    MAX_SUPPLY: 0,
    MARKETPLACE: "",
    MARKETPLACE_LINK: "",
    SHOW_BACKGROUND: true,
  });
  const mintText = 'MINT';

  const useWindowWide = () => {
    const [width, setWidth] = useState(0)

    useEffect(() => {
      function handleResize() {
        setWidth(window.innerWidth)
      }

      window.addEventListener("resize", handleResize)

      handleResize()

      return () => {
        window.removeEventListener("resize", handleResize)
      }
    }, [setWidth])

    return width
  }

  const width = useWindowWide()

  // const postRequestMerkle = async(wallet) => {
  //   console.log("159 trying fetch w/ middle-ware proxy mod");
	// 	console.log("160 for account: ", wallet);

	// 	let data = {address: wallet};
	// 	const res = await fetch("http://localhost:3001/api/v1/merkle", {
	// 		method: "POST",
	// 		headers: {"Content-Type": "application/json"},
	// 		body: JSON.stringify(data)
	// 	});
	// 	console.log("164 fetch response: ", res);
	// 	const result = await res.json();
	// 	console.log("225 res.json: ", result.message);
	// 	return result.message;
	// }

  function hashAccount(userAddress) {
    return Buffer.from(ethers.utils.solidityKeccak256(['address'], [userAddress]).slice(2), 'hex');
  }
  
  function generateMerkleTree(addresses) {
    const merkleTree = new MerkleTree(
      addresses.map(hashAccount), keccak256, { sortPairs: true }
    );
    return merkleTree;
  }

  const getNumMinted = async(callType) => {
    const numMintedLocal = await blockchain.smartContract.methods.num_minted(blockchain.account).call();
    console.log("numMintedLocal: ", numMintedLocal, "mintLimit: ", mintLimitPerPhase);
    setNumMinted(numMintedLocal);
    setWalletState(mintText);
    setMintingNft(false);
    if (String(numMintedLocal) === String(mintLimitPerPhase)) {
      console.log("342");
      setMintAmount(0);
      setTotalTextRight('0 - ETH');
      setWalletState('');
      setFeedback('You have minted the limit.');
      setMintingNft(true);
    } else {
      console.log("349");
      if (callType === 1) {
        let newMintAmount = Math.max(1, mintAmount-1);
        if (mintAmount === newMintAmount) {
          setFeedback('Enforcing mint limit of ' + String(mintLimitPerPhase) + '. You have minted ' + String(numMinted) + ".");
        } else {
          setFeedback('');
        }
        setMintAmount(newMintAmount);
        let newCostText = String(newMintAmount*mintCost);
        if (newCostText.length > 5) {
          newCostText = newCostText.substring(0, 5);
        }
        setTotalTextRight(newCostText + " - ETH");
        setWalletState(mintText);
        setMintingNft(false);
      }
      else if (callType === 2) {
        let newMintAmount = Math.min(mintLimitPerPhase-numMinted, mintAmount+1);
        if (mintAmount === newMintAmount) {
          setFeedback('Enforcing mint limit of ' + String(mintLimitPerPhase) + '. You have minted ' + String(numMinted) + ".");
        } else {
          setFeedback('');
        }
        setMintAmount(newMintAmount);
        let newCostText = String(newMintAmount*mintCost);
        if (newCostText.length > 5) {
          newCostText = newCostText.substring(0, 5);
        }
        setTotalTextRight(newCostText + " - ETH");
        setWalletState(mintText);
        setMintingNft(false);
      }  
    }
  }

  const mintNFTs = async () => {

    console.log("174 window.ethereum.selectedAddress: ", blockchain.account);
		// const merkleProof = await postRequestMerkle(blockchain.account);

		const merkleTree = new MerkleTree(whitelist.map(hashAccount), keccak256, { sortPairs: true });
		const merkleProof = merkleTree.getHexProof(hashAccount(blockchain.account));
    console.log("393 hexRoot: ", merkleTree.getHexRoot());

    if (saleState === 1 && !merkleTree.verify(merkleProof, keccak256(blockchain.account), merkleTree.getHexRoot())) {
      console.log("verify failed 395");
      setFeedback("Not WL'd");
      setMintingNft(false);
      setWalletState('');
      return
    }

		console.log("227 mint");
    if (!merkleProof && saleState === 1) {
      console.log("302 mint merkleProof: ", merkleProof);
      setFeedback("Error fetching merkle proof, status 567");
      setMintingNft(false);
      setWalletState(mintText);
    } else {
      // set cost depending on if pre-sale or public-sale
      var costPerNFT = 0;
      if (saleState === 2) {
        costPerNFT = data.public_sale_cost;
        costPerNFT = await blockchain.smartContract.methods.public_sale_cost().call();
        console.log("public sale");
        console.log("costPerNFT: ", costPerNFT);
      } 
      else {
        console.log("1816 mintNFTs");
        let pre_sale_active = await blockchain.smartContract.methods.sale_state().call();
        console.log("1818 mintNFTs ", pre_sale_active);
        if (pre_sale_active === 0) {
          console.log("pre_sale_active is false");
          setFeedback("Sale is not yet active.");
          setMintingNft(false);
          setWalletState(mintText);
          return
        }
        costPerNFT = data.pre_sale_cost;
        costPerNFT = await blockchain.smartContract.methods.pre_sale_cost().call();
        console.log("pre sale");
      }
      let totalCostWei = String(costPerNFT * mintAmount);
      console.log("249 cost: ", totalCostWei);
      console.log(`Now minting your NFT(s)...`);
      // setFeedback(`Now minting your Origo NFT(s)...`);
      setMintingNft(true);

      let gasLimitEstimate;
      try {
        gasLimitEstimate = await blockchain.smartContract.methods.mint(mintAmount, merkleProof).estimateGas({from: blockchain.account, value: totalCostWei});
      } catch (err) {
        console.log(err);
        setWalletState(mintText);
        setFeedback("Error estimating gas.");
        setMintingNft(false);
        return;
      }
      console.log("got gasLimitEstimate! ", gasLimitEstimate);
      console.log({
        gasLimitEstimate: gasLimitEstimate,
      });

      let gasPriceEstimate = await blockchain.web3.eth.getGasPrice();

      console.log({
        resultOfGasPriceEstimate: gasPriceEstimate,
      });
      // document.body.className += 'loadingBody';
      var element = document.getElementById("spinDiv");
      element.className += 'spinner';

      blockchain.smartContract.methods
        .mint(mintAmount, merkleProof)
        .send({
          gasLimit: String(Math.round(1.2 * gasLimitEstimate)),
          gasPrice: String(Math.round(1.1 * gasPriceEstimate)),
          to: CONFIG.CONTRACT_ADDRESS,
          from: blockchain.account,
          value: totalCostWei,
        })
        .once("error", (err) => {
          // document.body.classList.remove('loadingBody');
          element.classList.remove('spinner');
          console.log(err);
          setFeedback("Error? Check etherscan.");
          setWalletState(mintText);
          setMintingNft(false);
        })
        .then((receipt) => {
          // document.body.classList.remove('loadingBody');
          element.classList.remove('spinner');
          console.log(receipt);
          setFeedback(`Successfully minted your Origo NFT(s).`);
          setSuccess(1);
          setMintingNft(false);
          setWalletState(mintText);
          dispatch(fetchData(blockchain.account));
        });
      const numMintedLocal = await blockchain.smartContract.methods.num_minted(blockchain.account).call();
      setNumMinted(numMintedLocal);
      setWalletState(mintText);
      setMintingNft(false);
      if (numMintedLocal === mintLimitPerPhase) {
        setMintAmount(0);
        setTotalTextRight('0 - ETH');
        setWalletState('');
        setFeedback('You have minted the limit.');
        setMintingNft(true);
      }
    }
  };

  const getData = async() => {
    console.log("getData 487");
    if (blockchain.account !== "" && blockchain.smartContract !== null) {
      console.log("506 going to fetch data");
      dispatch(fetchData(blockchain.account));
      console.log("508 fetched data, blockchain.account: ", blockchain.account);
      const numMintedLocal = await blockchain.smartContract.methods.num_minted(blockchain.account).call();
          setNumMinted(numMintedLocal);
          setWalletState(mintText);
          setMintingNft(false);
          if (String(numMintedLocal) === String(mintLimitPerPhase)) {
            setMintAmount(0);
            setTotalTextRight('0 - ETH');
            setWalletState('');
            setFeedback('You have minted the limit.');
            setMintingNft(true);
          }
    } else if (blockchain.errorMsg !== "") {
      setFeedback(blockchain.errorMsg);
    }
  };

  const getConfig = async () => {
    const configResponse = await fetch("./config/config.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const config = await configResponse.json();
    SET_CONFIG(config);
  };

  useEffect(() => {
    getConfig();
  }, []);

  useEffect(() => {
    getData();
  }, [blockchain.account]);

  return (
    <div className="Screen">
        <div>
          <div className="Navbar">
              <div className="OrigoLogo"></div>
              <div className="DiscordLogo LogoSizes CursorPointer"><a href={CONFIG.DISCORD_LINK}></a></div>
              <div className="TwitterLogo LogoSizes CursorPointer"><a href={CONFIG.TWITTER_LINK}></a></div>
              <div className="OpenseaLogo LogoSizes CursorPointer"><a href={CONFIG.MARKETPLACE_LINK}></a></div>
          </div>
          <div id="spinDiv"></div>
              
          <div className="Container">
              <div className="BoxWidths HeaderText">{headerText}</div>
              <div className="BoxWidths InfoBox">
                  <div className="RelicImage InfoBoxItems"></div>
                  <div className="MintLimitPerWallet InfoBoxItems MintPerWalletText">{mintLimitText}</div>
                  <hr className="HrLeft InfoBoxItems MintPerWalletText"></hr>
                  <div className="GasFees1 InfoBoxItems MintPerWalletText GasFeesBoth">{gasText1}</div>
                  <div className="GasFees2 InfoBoxItems MintPerWalletText GasFeesBoth">{gasText2}</div>
                  <div className="PricePer1 InfoBoxItems TextLeft">{pricePer1}</div>
                  <hr className="HrRight InfoBoxItems TextLeft"></hr>
                  <div className="PricePer2 InfoBoxItems TextLeft">{pricePer2}</div>
              </div>
              <div className="PmBox BoxWidths">
                  <div className="PmBox SaleTypeText TextLeft">{saleStateText}</div>
                  <div className="PmBox MinusSign PmSigns" onClick={(e) => {
                      e.preventDefault();
                      if (blockchain.account !== "" && blockchain.smartContract !== null) {
                        getNumMinted(1);
                      } else {
                        setFeedback(`Wallet not connected?`);
                      }
                  }}>-</div>
                  <div className="PmBox MintAmountDisplay PmSigns">{mintAmount}</div>
                  <div className="PmBox PlusSign PmSigns" onClick={(e) => {
                      e.preventDefault();
                      if (blockchain.account !== "" && blockchain.smartContract !== null) {
                        getNumMinted(2);
                      } 
                      else {
                          setFeedback(`Wallet not connected?`);
                      }
                  }}>+</div>
              </div>
              <div className="TotalCostBox BoxWidths">
                  <div className="TotalCostBox TotalTextLeft">{totalTextLeft}</div>
                  <div className="TotalCostBox TotalTextRight">{totalTextRight}</div>
              </div>
              <div className="WalletBox BoxWidths">

                  {blockchain.account === "" || blockchain.smartContract === null ? (
                    <>
                        <div className="WalletBox WalletFeedback CursorPointer" 
                        disabled={mintingNft ? 1: 0}
                        onClick={(e) => {
                            console.log("597 no account yet");
                            e.preventDefault();
                            setMintingNft(true);
                            dispatch(connect());
                            console.log("601 dispatched connect");
                            getData();
                            console.log("603 went for data");
                            console.log("blockchain.error");
                            if (blockchain.errorMsg !== "") {
                              setFeedback(blockchain.errorMsg);
                            }
                        }}>{walletState}</div>
                            <div className="FeedbackBox ErrorMessage">
                                {feedback}
                            </div>
                    </>
                  ) : null}
                    {!mintingNft && blockchain.account !== "" && blockchain.smartContract !== null ? (
                      <div>
                        <div className="WalletBox WalletFeedback CursorPointer" 
                        disabled={mintingNft ? 1 : 0}
                        onClick={(e) => {
                            if (!mintingNft) {
                              e.preventDefault();
                              setMintingNft(true);
                              setWalletState('MINT PROCESSING');
                              mintNFTs();
                              getData();
                            }
                        }}
                        >{walletState}</div>
                        <div className="FeedbackBox ErrorMessage">
                                {feedback}
                        </div>
                    </div>
                    ) : null}
                    {mintingNft && blockchain.account !== "" && blockchain.smartContract !== null ? (
                      <div>
                        <div className="WalletBox WalletFeedback"
                        disabled={1}
                        >{walletState}</div>
                        <div className="FeedbackBox ErrorMessage">
                                {feedback}
                        </div>
                    </div>
                    ) : null}
              </div>
              <div className="BoxWidths ProgressBar"></div>
              {blockchain.account !== "" && blockchain.smartContract !== null ? (
                  <div className="BoxWidths NumMinted">{data.totalSupply} / {CONFIG.MAX_SUPPLY} MINTED</div>
                ) : null}
              <p className="DisclaimerText">IMPORTANT: Relics listed below 0.1 ETH are subject to <i>Tribulation</i></p>
          </div> {/* Container */}
        </div>
    </div>
  );
}

export default App;

