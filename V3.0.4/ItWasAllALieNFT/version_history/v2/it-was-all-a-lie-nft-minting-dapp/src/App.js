import './App.css';
import backgroundImageMobileBeforeMint from "./IMG_6623_words.png"
import backgroundImageDesktopBeforeMint from "./IMG_6611_words.png"
import backgroundImageMobile from "./IMG_6638.png"
import backgroundImageDesktop from "./IMG_6636.png"
import mintButtonImage from "./MintTransparency.png"
import mintedDisplayImage from "./MintedTransparency.png"
import openseaLogo from "./OpenseaTransparency.png"
import twitterLogo from "./TwitterTransparency.png"
import plusButtonImage from "./PlusTransparency.png"
import minusButtonImage from "./MinusTransparency.png"
import toMintIndicatorImage from "./IndicatorTransparency.png"
import mintedIndicatorImage from "./MintedIndicatorTransparency.png"
import useWindowDimensions from './WindowDimensions';
import { useState } from 'react'

function App() {
    const [mintAmount, setMintAmount] = useState(1)
    const [supplyMinted, setSupplyMinted] = useState("8888")

    const { height, width } = useWindowDimensions()

    async function handleMint() {
        console.log("handled mint click")
        return
    }

    async function handlePlusButton() {
        console.log("handled plus click")
        return
    }

    async function handleMinusButton() {
        console.log("handled minus click")
        return
    }


    console.log("h: ", height)
    console.log("w: ", width)
    console.log("w/h: ", width/height)

    let topDivHeight = 200
    let containerWidth = 420 
    let containerHeight = 400
    let top = 0
    let marginLeft = Math.round(0.36*width)
    let backgroundImage = `url(${backgroundImageDesktop})`
    if (height > width) {
        containerWidth = 360
        containerHeight = 320
        backgroundImage = `url(${backgroundImageMobile})`
        marginLeft = Math.round(0.19*width)
        topDivHeight = 150
        if (width < 900) {
          containerWidth = 360
          containerHeight = 320
          marginLeft -= Math.floor((900 - width)/8.0)
          containerWidth -= Math.floor((900 - width)/6.0)
          containerHeight -= Math.floor((900 - width)/6.0)
        }
    } else if (width < 1520) {
        containerWidth = 400
        containerHeight = 400
        containerWidth  -= Math.floor((1520-width)/4.0)
        containerHeight -= Math.floor((1520-width)/4.0)
    } else if (height < 1000) {
        containerWidth = 400
        containerHeight = 400
        marginLeft = Math.round(0.36*width)
        containerWidth  -= Math.floor((1000-height)/4.0)
        containerHeight -= Math.floor((1000-height)/4.0)
        marginLeft += Math.floor((1000-height)/4.0)
    }
    if (width > height && width/height > 1.593 && height < 1000) {
        console.log("in if")
        containerWidth = 400
        containerHeight = 400
        marginLeft = Math.round(0.36*width)
        containerHeight -= Math.floor((1000-height)/2.5)
        containerWidth -= Math.floor((1000-height)/2.5)
        marginLeft += Math.floor((1000-height)/4.0)
        if (width < 1520) {
          marginLeft -= Math.floor((1520-width)/5.0)
        }
    }
    let margin = "0 0 0 " + marginLeft + "px"
    console.log("margin: ", margin)
    console.log("topDivHeight: ", topDivHeight)

    return (
        <div className="screen" style={{ 
          backgroundImage:backgroundImage,
        }}>
            <a style={{
                marginLeft: Math.round(width/2)}} href="https://raritysniper.com/nft-drops-calendar"
            ></a>
            {height > width && 
              <div style={{
                  height: {topDivHeight} + "px",
                  width: 400
                }}></div>
            }
            <audio src="./itwasallalie_music.mp3" autoPlay loop></audio>
            <div className="container" style= {{
                margin: margin,
                width: containerWidth + "px",
                height: containerHeight + "px",
                backgroundColor: "transparent"
            }}>
            
                <div style={{display:"flex", direction:"row", justifyContent:"space-between"}}>
                    <a href="https://opensea.io" style={{marginTop: 10, marginLeft: 0, height:100, width:100, borderRadius:99999999}}><div className="OpenseaLogo" style={{ backgroundImage:`url(${openseaLogo})`}}></div></a>
                    <a href="https://twitter.com/itwasallalienft" style={{marginTop: 10, marginRight: 30, height:100, width:100, borderRadius:99999999}}><div className="TwitterLogo" style={{ backgroundImage:`url(${twitterLogo})`}}></div></a>
                </div>
                <div style={{display:"flex", direction:"row", justifyContent:"space-around"}}>
                      <div className="MintButton" style={{ backgroundImage:`url(${mintButtonImage})`}}
                          onClick={() => {handleMint()}}>
                      </div>

                      <div className="PlusButton" style={{ backgroundImage:`url(${plusButtonImage})`}}
                          onClick={() => {handlePlusButton()}}>
                      </div>
                      <div className="MinusButton" style={{ backgroundImage:`url(${minusButtonImage})`}}
                          onClick={() => {handleMinusButton()}}>
                      </div>
                      <div className="ToMintDisplay" style={{ backgroundImage:`url(${toMintIndicatorImage})`}}>
                          {mintAmount}
                      </div>
                  </div>
                  <div style={{display:"flex", direction:"row", justifyContent:"space-around"}}>
                      <div className="MintedDisplay" style={{ backgroundImage:`url(${mintedDisplayImage})`}}></div>
                      <div className="MintedIndicator" style={{ backgroundImage:`url(${mintedIndicatorImage})`}}>
                          {supplyMinted}
                      </div>
                  </div>
              </div>
            {/* <div className="MintButton" style={{ backgroundImage:`url(${mintButtonImage})`}}
              onClick={() => {mint()}}>
            </div> */}
        </div>
    );
}
export default App;