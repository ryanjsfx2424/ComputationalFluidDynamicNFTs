typ = "og"

ftxt = typ + ".txt"
with open(ftxt, "r") as fid:
  lines = fid.readlines()
# end with

lines2 = []
with open("whitelist_" + typ + ".json", "w") as fid:
  fid.write("[\n")
  for ii in range(len(lines)):
    line = lines[ii]

    if   "," in line:
      line = line.split(",")[0]
    elif "." in line:
      line = line.split(".")[1]
    # end if

    line = line.replace(" ","").replace("\n","")
    if ii != len(lines)-1:
      fid.write('  "' + line + '",\n')
    else:
      fid.write('  "' + line + '"\n')
  # end for
  fid.write("]")
# end with open
