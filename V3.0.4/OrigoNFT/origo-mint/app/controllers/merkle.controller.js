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
    });
    return;
  }

  const fpath = "./utils/whitelist/whitelisted_addresses.json";
  fs.readFile(fpath, function (err, data) {
    if (err) {
      console.log("16 merkle controller err: ", err);
      res.status(500).send({
        message: "cannot read whitelist.json :(",
      });
    } else {
      const whitelist = String(data).replaceAll("[", "").replaceAll("]", ""
                                   ).replaceAll('"', "").replaceAll("\n",""
                                   ).replaceAll(" ","").split(",");
      console.log("20 merkle controller wl: ", whitelist);
      const merkleTree = new MerkleTree(whitelist.map(hashAccount), keccak256, { sortPairs: true } );
      const merkleProof = merkleTree.getHexProof(hashAccount(req.body.address));
      console.log("45 hexRoot: ", merkleProof);
      console.log("46 merkleProof: ", merkleTree.getHexRoot());
      let verification = merkleTree.verify(merkleProof, keccak256(req.body.address), merkleTree.getHexRoot())
      console.log("47 verify: ", verification);
      console.log("48 wallet: ", req.body.address);

      if (!verification) {
        res.status(401).send({
          message: "bad merkle proof",
        })
      } else {
        res.status(200).send({message: merkleProof});
      }
    }
  });
  return
};
console.log("done w/ merkle controller js");
