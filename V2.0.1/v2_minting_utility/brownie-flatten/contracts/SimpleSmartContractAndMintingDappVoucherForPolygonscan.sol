// SPDX-License-Identifier: MIT

/*
This ERC-1155 token (polygon) was airdropped to wallets that 
minted two or more CFD NFTs V2.0.0.

This voucher can be redeemed for one simple NFT smart contract 
plus minting dapp (for collections with a potential maximum 
initial sales revenue of greater than $100,000 or greater than 
25 eth, I request 2% of the initial sales - this will be written
into the smart contract).

This voucher null and void after March 10th 2051 and where prohibited.
To redeem, send this token to 0x01656D41e041b50fc7c1eb270f7d891021937436
and send me a message on ToTheMoonsNFT discord or on twitter @TheLunaLabs.

ToTheMoons!
TheLunaLabs
*/

pragma solidity >=0.7.0 <0.9.0;

import "./ERC1155Supply.sol";
import "./Ownable.sol";

contract SimpleSmartContractAndMintingDappVoucher is ERC1155Supply, Ownable {

    // Contract name
    string public name;
    // Contract symbol
    string public symbol;

    constructor(
        string memory _name,
        string memory _symbol
    ) ERC1155("ipfs://QmZ96x5wGhCU6fStktTueK9cip9YXE6Xrou1oYnWR8kzrV/0.json") {
        name = _name;
        symbol = _symbol;
        _mint(msg.sender, 0, 10, "");
    }
}
