// const fetch = require("node-fetch")
import fetch from 'node-fetch';

(async () => {
  const response = await fetch("https://opensea.io/assets/ethereum/0xb716600ed99b4710152582a124c697a7fe78adbf/1")
  const data = await response.json()
  console.log(JSON.stringify(data, null, 2));
})();
