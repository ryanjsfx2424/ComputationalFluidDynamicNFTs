addresses = [
"0x64F1E48cb75825c384B8eB6134c959c3C8BBC11A",
      "0x0eE37690F00557930Beb57286b0cca7d85714B00",
      "0x0bB3F2c0673F56641E63C9E80Dc4D53d78f98A04",
]

addresses = 500*addresses
with open("whitelisted_addresses.json", "w") as fid:
  fid.write("[\n")
  for address in addresses:
    fid.write('  "' + address + '",\n')
  fid.write("]")
# end with open
