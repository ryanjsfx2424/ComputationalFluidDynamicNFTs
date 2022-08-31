import { useState, useEffect, Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import { 
	Flex,
	Image,
	Text,
	ChakraProvider,
	Spinner,
} from "@chakra-ui/react";
import "./App.scss";
import "./mdi/css/materialdesignicons.css";
import Aos from "aos";
import "aos/dist/aos.css";
import img1 from "./img1.png";
import img2 from "./img2.png";
import founder1 from "./founder1.png";
import founder2 from "./founder2.png";
import founder3 from "./founder3.png";
import founder4 from "./founder4.png";
import founder3small from "./founder3small.png";
import show1 from "./show1.png";
import show2 from "./show2.png";
import show3 from "./show3.png";
import show4 from "./show4.png";
import show5 from "./show5.png";
import show6 from "./show6.png";
import show7 from "./show7.png";
import show8 from "./show8.png";
import show9 from "./show9.png";
import show10 from "./show10.png";
import show11 from "./show11.png";
import show12 from "./show12.png";
import show13 from "./show13.png";
import show14 from "./show14.png";
import show15 from "./show15.png";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";
import icon from "./icon.png";
import { pinJSONToIPFS } from './pinata.js';
import { ethers } from "ethers";
import Web3 from "web3";
import Web3EthContract from "web3-eth-contract";

console.log("46 App.js");

require('dotenv').config();
const NETWORK_ID = 0x4; // Rinkeby
const NETWORK_NAME = "RINKEBY";
const alchemyKey = process.env.REACT_APP_ALCHEMY_KEY3;
const alchemyURL = process.env.REACT_APP_ALCHEMY_KEY;
const burner_priv_key = process.env.REACT_APP_ALCHEMY_KEY2;
const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
const web3 = createAlchemyWeb3(alchemyURL);
const contractABI = require('./contract-abi.json');
console.log("55 App abi: ", JSON.stringify(contractABI));
const contractAddress = "0xee40d1556a460c2b93e40F33EB8Ff0CEaCDD4838";
const ETHERSCAN_LINK = "https://rinkeby.etherscan.io/address/" + contractAddress;
const countDownDate = new Date("Aug 31, 2022 15:37:25").getTime();
const nftContract = new web3.eth.Contract(contractABI, contractAddress);

// const alchemyProvider = new ethers.providers.AlchemyProvider("rinkeby", alchemyKey);
// const signer = new ethers.Wallet(burner_priv_key, alchemyProvider);
// const smartContract = new ethers.Contract(contractAddress, contractABI, signer);


function App() {
	const [isConnected, setIsConnected] = useState(false)
	const [correctNetwork, setCorrectNetwork] = useState(false)
	const [userAddress, setUserAddress] = useState("")
	const [loading, setLoading] = useState(false)
	const [funcRes, setFuncRes] = useState("")
	const [funcRes2, setFuncRes2] = useState("")
	const [funcTrue, setFuncTrue] = useState(false)
	const [wlStart, setWlStart] = useState(countDownDate);

	useEffect(() => {
		Aos.init({ duration: 1500 });
	}, []);

	//TIMER FOR MINT COUNTDOWN
	useEffect(() => {
		// Update the count down every 1 second
		var x = setInterval(function() {
		// Get today's date and time
		var now = new Date().getTime();	
		// Find the distance between now and the count down date
		var distance = wlStart - now;	
		// Time calculations for days, hours, minutes and seconds
		var days = Math.floor(distance / (1000 * 60 * 60 * 24));
		var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((distance % (1000 * 60)) / 1000);	
		// Output the result in an element with id="demo"
		if(days === 1) {
			days = days + "day : "
		}
		else if(days === 0) {
			days = ""
		}
		else {
			days = days + "days : "
		}
		if(hours === "0") {
			hours = ""
		}
		else {
			hours = hours + "hrs : "
		}
		document.getElementById("launchTime").innerHTML = days + hours + minutes + "mins : " + seconds + "sec";	
		// If the count down is over, write some text 
		if (distance < 0) {
			clearInterval(x);
			document.getElementById("launchTime").innerHTML = "";
		}
		}, 1000);
	}, [])







	//CONNECT WALLET
	function walletListener() {
		if (window.ethereum) {
			window.ethereum.on("accountsChanged", (account) => {
			if (account.length > 0) {
				setUserAddress(account[0])
				setIsConnected(true)
				console.log("124 set is connected true");
			} else {
				setUserAddress(account[0])
				setIsConnected(false)
				alert("install metamask extension!!");
			}
			});
			window.ethereum.on("chainChanged", (chainId) => {
				if (Number(chainId) === NETWORK_ID) {
					setCorrectNetwork(true);
				} else {
					setCorrectNetwork(false);
					alert("change network to " + NETWORK_NAME);
				}
			})
		} else {
			alert("install metamask extension!!");
		}
	}
	useEffect(async () => {
		var account;
		try {
			account = await window.ethereum.request({method: 'eth_accounts'})
		}
		catch {
			console.log("error grabbing account");
			account = "";
		}
		if (account.length > 0) {
			var netId;
			try {
				netId = await window.ethereum.request({method: 'net_version'})
			}
			catch {
				console.log("error grabbing account");
				netId = -1;
			}
			setUserAddress(account[0])
			setIsConnected(true)
			if (netId === NETWORK_ID) {
				setCorrectNetwork(true)
			}
			else {
				setCorrectNetwork(false)
			}
		}
		else {
			setIsConnected(false)
			setCorrectNetwork(false)
		}
		walletListener()
	}, [])
	const btnhandler = () => {
	// Asking if metamask is already present or not
	if (window.ethereum) {
		// res[0] for fetching a first wallet
		window.ethereum
		.request({ method: "eth_requestAccounts" })
		.then((res) => accountChangeHandler(res[0]));
		window.ethereum.request({ method: "net_version"})
		.then((res) => networkChangeHandler(res[0]));
	} else {
		alert("install metamask extension!!");
	}
	};
	const accountChangeHandler = (account) => {
		setUserAddress(account)
		setIsConnected(true)
	};
	const networkChangeHandler = (netId) => {
		if (netId == NETWORK_ID) {
			setCorrectNetwork(true)
		}
	}


	const postRequestMerkle = async(wallet) => {
		console.log("159 trying fetch w/ middle-ware proxy mod");
		console.log("160 for account: ", wallet);

		let data = {address: wallet};
		const res = await fetch("/api/v1/merkle", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(data)
		});
		const result = await res.json();
		console.log("225 result: ", result);
		return [result.merkle,result.mintType];
	}

	//MINT FUNCTION
	const mintNFT = async() => {
		setLoading(true)

		Web3EthContract.setProvider(window.ethereum);
		let web3 = new Web3(window.ethereum);
		const SmartContractObj = new Web3EthContract(contractABI, contractAddress);

		try {
			let wl_start = await SmartContractObj.methods.wl_start().call();
			setWlStart(wl_start);
		} catch {
			console.log("error getting wl_start");
			return {
				success: false,
				status: "😥 Something went wrong fetching WL start time"
			}
		}

		var now = new Date().getTime();
		if (now - wlStart < 0) {
			console.log("tried to mint too early: ", now, wlStart, now-wlStart);
			return {
				success: false,
				status: "😥 No minting before WL sale starts!"
			}
		}

		let public_start;
		try {
			public_start = await SmartContractObj.methods.wl_start().call();
		} catch {
			console.log("error getting public_start");
			return {
				success: false,
				status: "😥 Something went wrong fetching public sale start time"
			}
		}

		console.log("174 window.ethereum.selectedAddress: ", window.ethereum.selectedAddress);
		let merkleProof = [];
		let mintAmount = 0;
		let mintCost = 0;
		if (now - public_start > 0) {
			// need to grab mint limit for gold, team/investor, og, wl depending on result
			const values = await postRequestMerkle(window.ethereum.selectedAddress);
			console.log("values: ", values);
			merkleProof = values[0];
			const mintType = values[1]; // 1 == gold, 2 == team/investor, 3 == og, 4 == fr, 5 == wl; -1 if none
			if (mintType === -1 || mintType === null) {
				console.log("mintType -1, address not in any merkle tree");
				return {
					success: false,
					status: "😥 Address not WL'd"
				}
			} else if (mintType === 1) {
				mintAmount = await SmartContractObj.methods.mint_limit_gold().call();
				console.log("mint Amount mt1: ", mintAmount);
			} else if (mintType === 2) {
				mintAmount = await SmartContractObj.methods.mint_limit_team().call();
				console.log("mint Amount mt2: ", mintAmount);
			} else if (mintType === 3) {
				mintAmount = await SmartContractObj.methods.mint_limit_og().call();
				console.log("mint Amount mt3: ", mintAmount);
			} else if (mintType === 4) {
				mintAmount = await SmartContractObj.methods.mint_limit_fr().call();
				console.log("mint Amount mt4: ", mintAmount);
			} else if (mintType === 5) {
				mintAmount = await SmartContractObj.methods.mint_limit_wl().call();
				console.log("mint Amount mt5: ", mintAmount);
				mintCost = await SmartContractObj.methods.cost_wl().call();
			} else {
				console.log("mintType not expected. Received: ", mintType);
				return {
					success: false,
					status: "😥 Error checking address vs WL, try again?"
				}
			}
		} else {
			// no merkle proof needed!
			try {
				mintAmount = await SmartContractObj.methods.mint_limit_public().call();
				mintCost   = await SmartContractObj.methods.cost_public().call();
			} catch {
				console.log("error getting mint limit public");
				return {
					success: false,
					status: "😥 Something went wrong fetching public mint limit"
				}
			}
		}
	
		console.log("227 mint");
		console.log("merkleProof: ", merkleProof);
		console.log("mintAmount: ", mintAmount);
		console.log("mintCost: ", mintCost);

		let gasLimitEstimate;
		try {
			gasLimitEstimate = await SmartContractObj.methods.mint(mintAmount, merkleProof).estimateGas({
				from: window.ethereum.selectedAddress,
				value: mintCost*mintAmount,
			})
		} catch (err) {
			console.log("265 mint err: ", err);
			return {
						success: false,
						status: "😥 Something went wrong: " + err.message
					}
		}
		console.log("got gasLimitEstimate! ", gasLimitEstimate);
		console.log({
			gasLimitEstimate: gasLimitEstimate,
		});

		let gasPriceEstimate = await web3.eth.getGasPrice();

		console.log({resultOfGasPriceEstimate: gasPriceEstimate});

		try {
			const receipt = await SmartContractObj.methods.mint(mintAmount, merkleProof).send({
				gasLimit: String(Math.round(1.2 * gasLimitEstimate)),
				gasPrice: String(Math.round(1.1 * gasPriceEstimate)),
				to: contractAddress,
				from: window.ethereum.selectedAddress,
				value: mintCost*mintAmount});
			console.log("293 mint receipt: ", receipt);
			return {
				success: true,
				status: receipt,
				status2: "SUCCESS",
			}
		}
		catch (err) {
			console.log("287 mint err", err);
			return {
				success: false,
				status: "😥 Something went wrong: Did not obtain merkle proof, status 567"
			}
		}
	}






	//MINT PRESS BUTTON
	const onMintPressed = async () => {
		const res = await mintNFT();
		storeRes(res)
	};
	async function storeRes(data) {
		setLoading(false)
		if(data.success) {
			setFuncRes(data.status2)
			setFuncRes2(data.status2)
			setFuncTrue(true)
		}
		else {
			alert(data.status)
			setFuncTrue(false)
		}
	}

	const showCase = [show1, show2, show3, show4, show5, show6, show7, show8, show9, show10, show11, show12, show13, show14, show15]

	return (
		<ChakraProvider>
			<Flex minHeight="100vh" w="100%" direction="column" bg="linear-gradient(290deg, rgb(20,20,50), rgb(40,40,120))" color="#fff" fontFamily="chalk" px={["4%", "6%"]} pt={["4%", "2.8%"]} pb={["8%", "2.8%"]}>
				<Flex px={["4", "12"]} w="100%" bg="rgba(255,255,255,0.07)" align="center" position="sticky" top="0" borderRadius="8px" mb="6" zIndex="1" data-aos="fade-up" backdropFilter="blur(4px)" py="3">
					<Flex align="center">
						<Image src={icon} w={["40px", "50px"]} h={["40px", "50px"]} />
						<Text fontWeight="bold" ml="3" display={["none", "block"]} textShadow="6px 2px rgb(70,70,70)" fontSize={["18px", "24px"]}>RDH Academy</Text>
					</Flex>
					<Flex flex="1" align="center" justify="flex-end">
						{
							(isConnected && correctNetwork) ?
							<>
								{userAddress?.substring(0, 4) + ".." + userAddress?.substring(userAddress?.length - 4, userAddress?.length)}
								<Flex ml="3" mr={["3", "7" ]} cursor="pointer" fontWeight="bold" border="1px solid #fff" py="3" borderRadius="8px" px="7" bg="rgba(255,255,255,0.2)" _hover={{ bg: "rgba(255,255,255,0.4)"}} display={["none", "flex"]} onClick={onMintPressed}>{loading ? <Spinner color="#fff" emptyColor="lightgrey" /> : "Mint Now"}</Flex>
							</>
							:
							<Flex mr={["3", "7" ]} cursor="pointer" fontWeight="bold" border="1px solid #fff" py="3" borderRadius="8px" px="7" bg="rgba(255,255,255,0.2)" _hover={{ bg: "rgba(255,255,255,0.4)"}} display={["none", "flex"]} onClick={btnhandler}>Connect Wallet</Flex>
						}

						<Flex mr={["3", "7" ]} cursor="pointer" fontWeight="bold" border="1px solid #fff" py="3" borderRadius="8px" px="7" bg="rgba(255,255,255,0.2)" _hover={{ bg: "rgba(255,255,255,0.4)"}} display={["none", "flex"]} onClick={() => {
							var a = document.getElementById('rdMap')
							a.scrollIntoView({behavior: "smooth"})
						}}>Roadmap</Flex>

						<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]} align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.9)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.7)"}} cursor="pointer"  mr={["3", "5" ]} onClick={() => window.open("https://twitter.com/RDHNFTs?s=21", "_BLANK")} color="#1DA1F2"><i className="mdi mdi-twitter"></i></Flex>


						<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]}  align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.9)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.7)"}} cursor="pointer"  color="#cd486b" mr={["3", "5" ]} onClick={() => window.open("https://www.instagram.com/rdhnfts/", "_BLANK")}><i className="mdi mdi-instagram"></i></Flex>

						<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]}  align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.9)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.7)"}} cursor="pointer" color="#7289da" onClick={() => window.open("https://discord.gg/rdhnft", "_BLANK")}><i className="mdi mdi-discord"></i></Flex>
					</Flex>
				</Flex>
						
				<Flex direction="column" py="4" data-aos="fade-down" px="5">
					<Text w="100%" fontSize={["20px", "40px"]} fontWeight="bold" textAlign="center" mb="2" mt="5">Minting In 🚀</Text>
					<Text w="100%" fontSize={["30px", "50px"]} fontWeight="bold" id="launchTime" textAlign="center"></Text>
				</Flex>

				<Flex w="100%" justify="space-between" mt={["6", "12"]} mb="6" align="center" overflowX="hidden"  className="bgStars" direction={["column", "row"]}>
					{
						(isConnected && correctNetwork) ?
						<>
							<Text display={["block", "none"]}>{userAddress?.substring(0, 4) + ".." + userAddress?.substring(userAddress?.length - 4, userAddress?.length)}</Text>
							<Flex ml="3" mb="6" cursor="pointer" fontWeight="bold" border="1px solid #fff" py="3" borderRadius="8px" px="7" bg="rgba(255,255,255,0.2)" _hover={{ bg: "rgba(255,255,255,0.4)"}} display={["flex", "none"]} onClick={onMintPressed}>Mint Now</Flex>
						</>
						:
						<Flex mb="6" cursor="pointer" fontWeight="bold" border="1px solid #fff" py="3" borderRadius="8px" px="7" bg="rgba(255,255,255,0.2)" _hover={{ bg: "rgba(255,255,255,0.4)"}} display={["flex", "none"]} onClick={btnhandler}>Connect Wallet</Flex>
					}
					<Flex w="100%" display={["flex", "none"]} mb="6" justify="space-between" align="center" data-aos="fade-left" className="bgStars2">
						<Image w="50%" src={img1} borderRadius="8px" className="mshake" />
						<Image w="45%" src={img2} borderRadius="8px" className="mshake2" />
					</Flex>

					<Flex w={["100%", "45%"]} direction="column">
						{
							funcTrue &&
							<Text data-aos="fade-up" mb="5" mt="2" border="1px solid #019401" py="3" borderRadius="8px" px="7" bg="rgba(14, 232, 14, .2)">Minted!! Check out your transaction on <Text textDecoration="underline" fontWeight="bold" cursor="pointer" onClick={() => window.open(ETHERSCAN_LINK)}>{ETHERSCAN_LINK}</Text></Text>
						}
						<Flex w="100%" direction="column" data-aos="fade-right" borderRadius="8px" py="6" mb="6">
							<Text fontWeight="bold" fontSize="30px" mb="4" textShadow="6px 2px rgb(70,70,70)">WHAT IS RDH? </Text>
							<Text fontSize={["16px", "17px"]}>
								<Flex mb="3" fontSize="25px" h="45px" w="45px" align="center" justify="center" borderRadius="100%" bg="rgb(80,80,130)" transition="300ms ease-in-out" _hover={{ bg: "rgb(100,100,150)"}} data-aos="fade-up" color="rgb(255, 0, 98)"><i className="mdi mdi-human-greeting"></i></Flex>

								<Text color="rgb(200,200,250)" mb="1" id="rdMap">Rekted diamond hands(RDH)</Text>Is a collection for the community and by the community, 5555 ERC-721 tokens randomly generated on the ethereum blockchain. We aim to be a source of light for rekt hodlers in the dark tunnel of the bear season, FOMO in to get your rekted bags pumped. 
							</Text>
						</Flex>
						
						<Flex w="100%" direction="column" data-aos="fade-right" bg="rgba(255,255,255,0.05)" borderRadius="8px" px={["6", "8"]} py="6">
							<Text fontSize={["16px", "17px"]}>
								<Flex mb="3" fontSize="20px" h="45px" w="45px" align="center" justify="center" borderRadius="100%" bg="rgb(80,80,130)" transition="300ms ease-in-out" _hover={{ bg: "rgb(100,100,150)"}} data-aos="fade-up" color="rgb(255, 213, 0)"><i className="mdi mdi-car-wash"></i></Flex>

								<Text color="rgb(200,200,250)" mb="1">Roadmap</Text>
								Only roadmap we have is to keep building based on hodlers interaction and incorporate feedback from our community.
							</Text>
						</Flex>
					</Flex>
					
					<Flex w="55%" display={["none", "flex"]} justify="space-between" align="center" data-aos="fade-left" pb="15%" pl="5%">
						<Image w="50%" src={img1} borderRadius="10px"  className="shake" />
						<Image w="45%" src={img2} borderRadius="10px" className="shake2" />
					</Flex>
				</Flex>


				<Flex mt={["6", "12"]} mb="6" bg="rgba(255,255,255,0.03)" w={["100vw", "100%"]} py={["6", "12"]} borderRadius={["0px", "8px"]} data-aos="fade-up" className="absW" px={["5%", "15%"]} direction="column" align="center">
					<Flex w="100%" direction="column" display={["none", "flex"]} align="flex-start">
						<Text mb="2" fontSize={["20px", "25px"]} fontWeight="bold" data-aos="fade-right">RDH Sneak Peeks</Text>
						<Text mb="12" textAlign="left" px={["2", "0%"]} pr={["0", "20%"]} data-aos="fade-left">
							All items in this collection will represent the experience a holder encountered in his/her Cypto/NFT journey.<br/>
							Represent your journey!
						</Text>
					</Flex>
					<Flex align="center" w="100%" justify="center">
						<Carousel
							autoPlay={true}
							infiniteLoop={true}
							showStatus={false}
							showIndicators={true}
							swipeable={true}
							showArrows={true}
							showThumbs={false}
							stopOnHover={false}
							interval={4000}
						>
							{
								showCase.map((item, index) => (
									<Flex w="100%" px={["1%", "25%"]} key={index} align="center" direction="column">
										<Image src={item} key={index} borderRadius="8px" className="carImg shake" />
									</Flex>
								))
							}
						</Carousel>
					</Flex>
					<Flex w="100%" direction="column" display={["flex", "none"]} align="center" overflowX="hidden">
						<Text mt="12" mb="2" fontSize={["20px", "25px"]} fontWeight="bold" data-aos="fade-right">RDH Sneak Peeks</Text>
						<Text textAlign="center" px={["2", "20%"]} data-aos="fade-left">
							All items in this collection will represent the experience a holder encountered in his/her Cypto/NFT journey.<br/>
							Represent your journey!
						</Text>
					</Flex>
				</Flex>

				<Flex justify="center" mt={["6", "12"]} backgroundColor="rgba(255,255,255,0.03)" borderRadius="8px" py="12" className="bgStars">
					<Flex w="100%" direction="column" align="center">
						<Text fontWeight="bold" fontSize={["24px", "30px"]}>
							The RDH Founders
						</Text>
						<Flex w="100%" align="center" justify="center" px="10%" direction={["column", "row"]}>
							<Flex direction="column" align="center" w={["100%", "50%"]} mb={["5", "0"]}>
								<Image w={["170px", "200px"]} h={["170px", "200px"]} borderRadius="100%" src={founder1} mt="6" data-aos="fade-up" />
								<Text textAlign="center" px={["2%", "10%"]} mt="6" data-aos="fade-up">
								<Text color="rgb(200,200,250)" cursor="pointer" mb="2" onClick={() => window.open("https://twitter.com/solsmahneth?s=21&t=_O59LWK2c3h6KY31ZgkOxw", "_BLANK")}>@Solsmahn.eth</Text>
								Also known as Tulipman in the community, Solsmahn is a UAE based Blockchain developer and NFT consultant
								</Text>
							</Flex>

							<Flex direction="column" align="center" w={["100%", "50%"]} mb={["5", "0"]}>
								<Image w={["170px", "200px"]} h={["170px", "200px"]} borderRadius="100%" src={founder2} mt="6" data-aos="fade-up" />
								<Text textAlign="center" px={["2%", "10%"]} mt="6" data-aos="fade-up">
								<Text color="rgb(200,200,250)" cursor="pointer" mb="2" onClick={() => window.open("https://twitter.com/mastrodre", "_BLANK")}>@Mastrodre</Text>
								Also known as OG kelvin is a Dubai based web 3 enthusiast and investor.
								</Text>
							</Flex>
						</Flex>

						<Flex align="center" w="100%" px="10%" direction={["column", "row"]}>
							<Flex w={["100%", "50%"]} direction="column" align="center" mb={["2", "0"]}>
								<Text fontWeight="bold" fontSize={["24px", "30px"]} mt={["12", "100px"]} mb="2" data-aos="fade-up">
									Advisor
								</Text>

								<Flex w="100%" align="center" justify="center" px="10%" direction={["column", "row"]}>
									<Flex direction="column" align="center" w={["100%", "50%"]}>
										<Image w={["170px", "200px"]} h={["170px", "200px"]} borderRadius="100%" src={founder3} mt="6" data-aos="fade-up" />
										<Image w="100px" h="100px" src={founder3small} position="absolute" borderRadius="100%" ml={["150px", "130px"]} mt="20px" boxShadow="0px 0px 8px rgb(0,0,0)" />
										<Text textAlign="center" px={["2%", "10%"]} mt="6" data-aos="fade-up">
										<Text color="rgb(200,200,250)" cursor="pointer" mb="2" onClick={() => window.open("https://twitter.com/shahh?s=21", "_BLANK")}>@Shahh</Text>
										</Text>
									</Flex>
								</Flex>
							</Flex>

							<Flex w={["100%", "50%"]} direction="column" align="center">
								<Text fontWeight="bold" fontSize={["24px", "30px"]} mt={["12", "100px"]} mb="2" data-aos="fade-up">
									Developer
								</Text>

								<Flex w="100%" align="center" justify="center" px="10%" direction={["column", "row"]}>
									<Flex direction="column" align="center" w={["100%", "50%"]}>
										<Image w={["170px", "200px"]} h={["170px", "200px"]} borderRadius="100%" src={founder4} mt="6" data-aos="fade-up" />

										<Text textAlign="center" px={["2%", "10%"]} mt="6" data-aos="fade-up">
										<Text color="rgb(200,200,250)" cursor="pointer" mb="2" onClick={() => window.open("https://twitter.com/thelunalabs?s=11&t=26eD2Z6tX4ktKWIeAkj7kg", "_BLANK")}>@TheLunaLabs</Text>
										</Text>
									</Flex>
								</Flex>
							</Flex>
						</Flex>
					</Flex>
				</Flex>
				
				<Flex direction="column" mt={["6", "12"]} bgColor="rgba(255,255,255,0.03)" borderRadius="8px" py="12" px={["6", "0"]}>
					<Text textAlign="center"  data-aos="fade-up">Created by the RDH founders with special love to our community, Our friends, families, and loved ones</Text>
					<Text textAlign="center" mt="3"  data-aos="fade-up">For all press inquiries, please contact <Text as="span" color="rgb(200,200,250)" mb="2">press@rdh.club</Text></Text>
					
					<Flex flex="1" align="center" justify="center" mt="8"  data-aos="fade-up">
					<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]} align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.1)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.3)"}} cursor="pointer" className="bounce" mr={["3", "5" ]} onClick={() => window.open("https://twitter.com/RDHNFTs?s=21", "_BLANK")}><i className="mdi mdi-twitter"></i></Flex>

					<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]}  align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.1)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.3)"}} className="bounce" mr={["3", "5" ]} cursor="pointer" onClick={() => window.open("https://discord.gg/rdhnft", "_BLANK")}><i className="mdi mdi-discord"></i></Flex>

					<Flex fontSize={["18px", "20px"]} h={["40px", "45px"]} w={["40px", "45px"]}  align="center" justify="center" borderRadius="100%" bg="rgba(255,255,255,0.1)" transition="300ms ease-in-out" _hover={{ bg: "rgba(255,255,255,0.3)"}} className="bounce2" onClick={() => window.open("https://www.instagram.com/rdhnfts/", "_BLANK")} cursor="pointer"><i className="mdi mdi-instagram"></i></Flex>
					</Flex>
				</Flex>
			</Flex>
		</ChakraProvider>
	)
}

export default App;
