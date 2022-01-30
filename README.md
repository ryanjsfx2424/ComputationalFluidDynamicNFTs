# ComputationalFluidDynamicNFTs
Steps:
   1) in THE\_ARGO\_NFT execute (python3) the\_executer.py
   2) Upload movies to IPFS (e.g., using pinata)
   3) Grab the link and adjust the generate\metadata and prereveal\_json
      scripts then run them.
   4) Upload metadata to IPFS.
   5) Copy-paste the smart contract (.sol file) into remix, change name
      of file and name of Contract function accordingly. Also READ
      the contract and modify for your use case.
   6) When you're done reading/modifying the .sol file, save it locally,
      go to the compiler section and turn on Auto compile and Enable
      optimization (I leave it at default 200). Also note the compiler
      version. Also change the "CONTRACT" box from Address to your contract
      name. Make sure your code compiles!
   7) Go to the deployment tab and change environment to Injected Web3
      - change your network to the correct one before proceeding!
   8) Select your contract in the CONTRACT drop-down menu.
   9) Click down arrow next to DEPLOY and fill out \_NAME, \_SYMBOL,
      _INITBASEURI, and _INITNOTREVEALEDURI_. For the URIs, grab them
      from pinata. Make sure to end those URIs with a forward slash!!
      (forward slash == "/" without the quotes).
  10) BEFORE clicking on transact, click the "copy" button next to it
      and save the bytecode in a text file somewhere.
  11) Then hit transact, test functionality such as minting (un-pause for that).
So I unpaused minting but couldn't get it to mint. I think it has to do with
how I wasn't going to allow the owner to mint (I tried on a different account
tho).

So I updated the contract to allow the owner to mint again and changed
the name of the contract to v002. Still uses IPFS of v001...

v002 and v003 called the contructor for v001 for some reason. Going
to quit out of brave and try again.

v004 at least everything was calling v004 functions but still didn't
let me mint. So I'm going back to Rinkeby for v005 and maybe I'll
just use regular polygon for v006 and burn the nfts after testing...

v005 deployed on Polygon but still no dice. I think either setting
pause to false isn't working (maybe needs cap locked?) or
it's the fact that I say the price is in ether and it should
actually be matic (although I don't think hashlips changed that
in the vid...)

v006 will try Rinkeby again. If that still fails, it has to do
with something I changed (maybe removing renounce ownership??)

Still refusing to mint...Watch hashlips vid, possibly grab fresh
contract from him and try again.

Watched it. I'll just grab a fresh contract from him.

That worked! (v007). Going to change collection name to CFD v(etc)
since typing it out breaks page. Also going to change piece names
to #(number) and colormap name. Also the description didn't show up...
so probably I messed up on pinata somehow...

v008 will adjust the metadata names to be #(num) + colormap and
change the...
So the hidden files look better. But it won't let me mint when
using another account...maybe b/c I removed the hashlips withdrawal?
I'll try copying fresh from his file again and minimally modifying it.
  AAAAH it was failing because I wasn't putting in a value... so this
probably would've worked if I had deployed on the minting dapp...

Okay so v009 will do some v001 edits.
It worked!

v0.0.10 will use the Mumbai testnet (otherwise same contract).
Mostly worked! #16 stayed hidden forever b/c I number 0-15 whereas
tokenIds are 1-index (lame). So, I need to change the baseURI to
be token-1.

v0.0.11 will test on Polygon (yes mainnet). I'll make sure to verify
the smart contract before minting - and only mint on the website like
for the real deal. Also going to update the website favicon and some
stuff.

v0.0.11 remix snafu'd: polygon said it had deployed but the contract
remained "pending creation" on remix.

v0.0.12 I tried again and increased the gas and it worked!
I then verified the contract on Polygon scan. Now I'm updating
the minting dapp so I copied the ppt that I take screenshots of
for the title image ("logo") and the background -- which I decided to be
blank for simplicity.


  12) minting dapp
  13) profit???


