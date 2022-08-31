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
  const [headerText, setHeaderText] = useState(`Origo Whitelist Sale`);
  const [mintLimitText, setMintLimitText] = useState(`2 Per Wallet`);
  const [pricePer1, setPricePer1] = useState(`Price Per Relic`);
  const [pricePer2, setPricePer2] = useState(`0.089 - ETH`);
  const [saleState, setSaleState] = useState(1);
  const [mintLimitPerPhase, setMintLimitPerPhase] = useState(2);
  const [saleStateText, setSaleStateText] = useState(`Whitelist Sale`);
  const [totalTextLeft, setTotalTextLeft] = useState(`Total`);
  const [totalTextRight, setTotalTextRight] = useState(`0.089 - ETH`);
  const [mintCost, setMintCost] = useState(0.089);
  const [mintAmount, setMintAmount] = useState(1);
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

  const mintNFTs = async () => {

    console.log("174 window.ethereum.selectedAddress: ", blockchain.account);
		// const merkleProof = await postRequestMerkle(blockchain.account);

		const merkleTree = new MerkleTree(whitelist.map(hashAccount), keccak256, { sortPairs: true });
		const merkleProof = merkleTree.getHexProof(hashAccount(blockchain.account));

    if (!merkleTree.verify(merkleProof, keccak256(blockchain.account), merkleTree.getHexRoot())) {
      console.log("verify failed");
      setFeedback("Not WL'd");
      return
    }

		console.log("227 mint");
    if (!merkleProof) {
      console.log("302 mint merkleProof: ", merkleProof);
      setFeedback("Error fetching merkle proof, status 567");
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
    setWalletState(`BUSY`);
    setMintingNft(true);

    let gasLimitEstimate;
    try {
      gasLimitEstimate = await blockchain.smartContract.methods.mint(mintAmount, merkleProof).estimateGas({from: blockchain.account, value: totalCostWei});
    } catch (err) {
      console.log(err);
      setWalletState(`ERROR`);
      setFeedback(err.message.split("{")[0] + ". Refresh page.");//"Error estimating gas. Bad merkle proof or tried to mint more than the pre/public sale limit. Refresh the page to try again.");
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
        console.log(err);
        setFeedback("Error? Check etherscan.");
        setWalletState('ERROR');
        setMintingNft(false);
      })
      .then((receipt) => {
        console.log(receipt);
        setFeedback(`Successfully minted your Origo NFT(s).`);
        setSuccess(1);
        setMintingNft(false);
        setWalletState(`SUCCESS`);
        dispatch(fetchData(blockchain.account));
      });
    }
  };

  const getData = () => {
    if (blockchain.account !== "" && blockchain.smartContract !== null) {
      dispatch(fetchData(blockchain.account));
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
        {/* <div className="Navbar">
            <div>
                <StyledOrigo alt={"origo logo"} src={"./config/images/origo-logo.png"} />
            </div>

            <a href={CONFIG.TWITTER_LINK}>
                <StyledTwitter alt={"twitter link"} src={"./config/images/twitter1.png"} />
            </a>

            <a href={CONFIG.DISCORD_LINK}>
                <StyledDiscord alt={"discord link"} src={"./config/images/discord1.png"} />
            </a>

            <a href={CONFIG.MARKETPLACE_LINK}>
                <StyledOpensea alt={"opensea link"} src={"./config/images/os1.png"} />
            </a>
        </div>         */}

        <div>
          <div className="Navbar">
              <div className="OrigoLogo"></div>
              <div className="DiscordLogo LogoSizes CursorPointer"><a href={CONFIG.DISCORD_LINK}></a></div>
              <div className="TwitterLogo LogoSizes CursorPointer"><a href={CONFIG.TWITTER_LINK}></a></div>
              <div className="OpenseaLogo LogoSizes CursorPointer"><a href={CONFIG.MARKETPLACE_LINK}></a></div>
          </div>
              
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
                      let newMintAmount = Math.max(1, mintAmount-1);
                      setMintAmount(newMintAmount);
                      setTotalTextRight(String(newMintAmount*mintCost) + " - ETH");
                  }}>-</div>
                  <div className="PmBox MintAmountDisplay PmSigns">{mintAmount}</div>
                  <div className="PmBox PlusSign PmSigns" onClick={(e) => {
                      e.preventDefault();
                      let newMintAmount = Math.min(mintLimitPerPhase, mintAmount+1);
                      setMintAmount(newMintAmount);
                      setTotalTextRight(String(newMintAmount*mintCost) + " - ETH");
                  }}>+</div>
              </div>
              <div className="TotalCostBox BoxWidths">
                  <div className="TotalCostBox TotalTextLeft">{totalTextLeft}</div>
                  <div className="TotalCostBox TotalTextRight">{totalTextRight}</div>
              </div>
              <div className="WalletBox BoxWidths">

                  {blockchain.account === "" || blockchain.smartContract === null ? (
                    <>
                        <div className="WalletBox WalletFeedback CursorPointer" onClick={(e) => {
                            e.preventDefault();
                            dispatch(connect());
                            getData();
                        }}>{walletState}</div>

                        {blockchain.errorMsg !== "" ? (
                            <div className="FeedbackBox ErrorMessage">
                                {blockchain.errorMsg}
                            </div>
                        ) : null}
                    </>
                  ) : null}
                    {feedback === `` && blockchain.account !== "" && blockchain.smartContract !== null ? (
                      <div>
                        <div className="WalletBox WalletFeedback CursorPointer" 
                        disabled={mintingNft ? 1 : 0}
                        onClick={(e) => {
                            e.preventDefault();
                            mintNFTs();
                            getData();
                        }}>{mintingNft ? "BUSY" : "MINT"}</div>
                    </div>
                    ) : null}
                    {feedback !== `` && blockchain.account !== "" && blockchain.smartContract !== null ? (
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
              <p className="DisclaimerText">IMPORTANT: Relics listed below mint are subject to <i>Tribulation</i></p>
          </div> {/* Container */}
        </div>
    </div>
  );
}

export default App;

