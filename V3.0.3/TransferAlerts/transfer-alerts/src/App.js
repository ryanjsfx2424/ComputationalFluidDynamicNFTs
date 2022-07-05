import logo from './logo.svg';
import './App.css';

(async () => {
  const response = await fetch("https://opensea.io/assets/ethereum/0xb716600ed99b4710152582a124c697a7fe78adbf/1")
  const data = await response.json()
  console.log(JSON.stringify(data, null, 2));
})();

function App() {
  const apiGet = () => {
    fetch("https://opensea.io/assets/ethereum/0xb716600ed99b4710152582a124c697a7fe78adbf/1").then((response) => response.json()).then((json) => console.log(json));
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>My API <br />
          <button onClick={apiGet}>Fetch API</button>
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
