import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";
import { render } from '@testing-library/react';

class App extends React.Component {
  constructor() {
    super();
    if (window.performance) {
      if (performance.navigation.type === 1) {
        var dice1 = Math.floor(Math.random()*6+1);
        var dice2 = Math.floor(Math.random()*6+1);

        if (dice1 > dice2) {
          this.h1text = "🚩 Player 1 Wins!";
        } else if (dice2 > dice1) {
          this.h1text = "Player 2 Wins! 🚩";
        } else {
          this.h1text = "Draw";
        }
        this.img1src = "/images/dice" + dice1 + ".png";
        this.img2src = "/images/dice" + dice2 + ".png";
      } 
      else {
        this.h1text = "Refresh Me";
        this.img1src = "../images/dice6.png";
        this.img2src = "../images/dice6.png";
      }
    }
  }

  render() {
    return (
      <>
        <div className="container">
          <h1>{this.h1text}</h1>
          <div className="dice">
            <p>Player 1</p>
            <img className="img1" src={this.img1src}></img>
          </div>
          <div className="dice">
            <p>Player 2</p>
            <img className="img2" src={this.img2src}></img>
          </div>
        </div>
        <footer>
          www 🎲 App Brewery 🎲 com
        </footer>
      </>
    )
  }
}

// function App() {
//   const [count, setCount] = useState(0);

//   console.log(count);
//   if (count < 20) {
//     setCount(count + 1);
//     return (
//       <>
//         <div className="container">
//           <h1>Refresh Me</h1>
//           <div className="dice">
//             <p>Player 1</p>
//             <img className="img1" src="../images/dice6.png"></img>
//           </div>
//           <div className="dice">
//             <p>Player 2</p>
//             <img className="img2" src="../images/dice6.png"></img>
//           </div>
//         </div>
//         <footer>
//           www 🎲 App Brewery 🎲 com
//         </footer>
//       </>
//     );
//   } else {
//     var dice1 = Math.floor(Math.random()*6+1);
//     var dice2 = Math.floor(Math.random()*6+1);
//     var h1text;

//     if (dice1 > dice2) {
//       h1text = "🚩 Player 1 Wins!";
//     } else if (dice2 > dice1) {
//       h1text = "Player 2 Wins! 🚩";
//     } else {
//       h1text = "Draw";
//     }
//     var img1src = "/images/dice" + dice1 + ".png";
//     var img2src = "/images/dice" + dice2 + ".png";

//     return (
//       <>
//         <div className="container">
//           <h1>{h1text}</h1>
//           <div className="dice">
//             <p>Player 1</p>
//             <img className="img1" src={img1src}></img>
//           </div>
//           <div className="dice">
//             <p>Player 2</p>
//             <img className="img2" src={img2src}></img>
//           </div>
//         </div>
//         <footer>
//           www 🎲 App Brewery 🎲 com
//         </footer>
//       </>
//     );
//   }
// }

export default App;
