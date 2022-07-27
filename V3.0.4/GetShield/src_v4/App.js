import React, { useEffect, useState, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { connect } from "./redux/blockchain/blockchainActions";
import { fetchData } from "./redux/data/dataActions";
import * as s from "./styles/globalStyles";
import styled from "styled-components";

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

export const ResponsiveWrapper = styled.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: stretched;
  align-items: stretched;
  width: 100%;
  @media (min-width: 767px) {
    flex-direction: row;
  }
`;

export const StyledLogo = styled.img`
  padding-top: 480px;
  width: 400px;
  @media (min-width: 156px) {
    width: 400px;
  }
  transition: width 0.1s;
  transition: height 0.1s;
`;


function App() {
  const dispatch = useDispatch();
  const blockchain = useSelector((state) => state.blockchain);
  const data = useSelector((state) => state.data);
  const [scanCounterUser,   setScanCounterUser]   = useState(0);
  const [scanCounterGlobal, setScanCounterGlobal] = useState(0);
  const [contractAddress, setContractAddress] = useState(``);  
  
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
    MAX_SUPPLY: 1,
    WEI_COST: 0,
    DISPLAY_COST: 0,
    GAS_LIMIT: 0,
    MARKETPLACE: "",
    MARKETPLACE_LINK: "",
    SHOW_BACKGROUND: false,
  });

  const getData = () => {
    if (blockchain.account !== "" && blockchain.smartContract !== null) {
      dispatch(fetchData(blockchain.account));
    }
  };

  const getConfig = async () => {
    const configResponse = await fetch("/config/config.json", {
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
  });

  useEffect(() => {
    getData();
  }, [blockchain.account]);

  const searchContract = () => {
    var data = new FormData();

    data.append("contract", document.getElementsByClassName("inputBox").value);
    console.log(data)
    for (let [k,v] of data.entries()) {
      console.log(k, v);
      return false;
    }
  }

  return (
    <s.Screen>
      <s.Container

        flex={1}
        ai={"center"}
        style={{ padding: 0, backgroundColor: "var(--primary)" }}
        image={CONFIG.SHOW_BACKGROUND ? "/config/images/bg.png" : null}
      >
        <s.Con
          className="ContainerGridBox">
          
          {/* First box */}
          <s.smallCon
            className="mainBox">
            <s.logoCon>
              <StyledLogo alt={"logo"} src={"/config/images/shieldLogoWhiteNoText.png"} />
              <s.TextDescription
                    style={{
                      textAlign: "center",
                      color: "var(--accent-text)",
                    }}
                  >
                    {`Scan any contract for malicious activity`}
                </s.TextDescription>
                <s.SpacerSmall></s.SpacerSmall>
                <div className="searchContainer">
                  <form onSubmit = {(e) => {
                    console.log(e);
                    console.log(e.target.value);
                    console.log(contractAddress);
                  }}>
                    <input className="inputBox" type= 'search' placeholder="Search Contracts / Addresses" onChange={(e) => {setContractAddress(e); console.log(contractAddress);}} />
                    <button className="searchButton" type="submit"><i className="fa fa-search"></i></button>
                  </form>
                </div>
                
            </s.logoCon>
            
          </s.smallCon>
          {/* End */}
        </s.Con>
        <s.SpacerMedium/>
      </s.Container >
    </s.Screen >


  );
}

export default App;
