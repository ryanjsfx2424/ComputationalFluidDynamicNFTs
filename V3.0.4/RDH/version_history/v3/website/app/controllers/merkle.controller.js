const perfy = require("perfy");
const fs = require("fs");
const{ MerkleTree } = require("merkletreejs");
const ethers = require("ethers");
const keccak256 = require("keccak256");

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

// Create and Save a new Analysis
exports.proof = async (req, res) => {
  // Validate request
  console.log("7 merkle.proof");
  console.log("8 merkle.proof, req.body: ", req.body);
  if (!req.body.address) {
    console.log("9 merkle.proof no address");
    res.status(400).send({
      message: "wallet address can not be empty!",
      proof: [],
      mintType: -1
    });
    console.log("34 sent 400");
    return;
  }
  const wallet = req.body.address;
  console.log("37 merkle.proof wallet: ", wallet);

  const fbase = "./utils/whitelist/whitelist_";
  const fext = ".json"
  const names = ["gold", "team", "og", "fr", "wl"]
  var fpath;
  var verify_flag = false;
  for (let ii = 1; ii < (names.length+1); ii++) {
    fpath = fbase + names[ii-1] + fext;
    console.log("44 merkle.proof ii, names[ii-1], :", ii, names[ii-1], fpath);
    var whitelist;
    fs.readFile(fpath, function (err, data) {
      if (err) {
        console.log("43 error reading file ii, fs[ii], fpath: ", ii, names[ii], fpath);
      } else {
        whitelist = String(data ).replaceAll("[", "").replaceAll("]", ""
                                      ).replaceAll('"', "").replaceAll("\n",""
                                      ).replaceAll(" ",  "").split(",");
        console.log("whitelist: ", whitelist);
      }
      var merkleTree = new MerkleTree(whitelist.map(hashAccount), keccak256, { sortPairs: true } );
      var merkleProof = merkleTree.getHexProof(hashAccount(wallet));

      console.log("45 hexRoot for fpath: ", merkleTree.getHexRoot(), fpath);
      console.log("46 merkleProof: ", merkleProof);

      var verification = merkleTree.verify(merkleProof, keccak256(wallet), merkleTree.getHexRoot())
      console.log("47 verify: ", verification);
      console.log("48 wallet: ", req.body.address);

      if (verification) {
          res.status(200).send({message: "Success!", merkle: merkleProof, mintType:ii});
          console.log("69 sent 200")
          verify_flag = true;
          return;
      }
    });
  }
};
console.log("done w/ merkle controller js");