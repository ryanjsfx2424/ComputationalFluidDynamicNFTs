with open("src/whitelisted_addresses.json", "r") as fid:
  lines = fid.readlines()
# end with open

with open("utils/whitelist/whitelisted_addresses.json", "w") as fid:
  fid.write("[\n")
  for ii,line in enumerate(lines):
    address = line.replace("\n","").replace("'","").replace('"',"").replace(",","").replace(" ","")

    good_address = "0x1A3a1A68f995cF23ddb0bc0777e2f7e9162F7855"
    if len(address) != len(good_address):
      print("bad address: ", address)
      print("len bad  add: ", len(address))
      print("len good add: ", len(good_address))
      input(">>")
      continue
    # end if

    if ii == len(lines)-1:
      fid.write('  "' + address + '"\n')
    else:
      fid.write('  "' + address + '",\n')
    # end if/else
  # end for
  fid.write("]")
# end with open
