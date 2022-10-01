## modify_metadata.py
import os

base = os.getcwd()
newdir = "json3"
os.system("mkdir -p " + base + "/" + newdir)
os.chdir(base + "/json")

i1 = 0
i2 = 0
i3 = 0
gold_cnt = 0
og_cnt = 55
reg_cnt = 498
for ii in range(1,5555+1):
  fname = base + "/json/" + str(ii) + ".json"
  print("fname: ", fname)

  with open(fname, "r") as fid:
    lines = fid.readlines()
  # end with

  old_cid = "QmYhGAkzMWmqB3BUzDsAXifHtatrXbtGPjYQNGr6srttDT"
  new_cid = "bafybeifxvxx3uegxmddht6s54jlxnp5rnxqbt4szp3r2e6tetpjxcfkici"
  lines[3] = lines[3].replace(old_cid, new_cid)

  lines[1] = lines[1].split(":")[0] + ': "Walking dark elves",\n'
  lines[2] = lines[2].split(":")[0] + ': "",\n'

  if len(lines) > 18:
    lines[18] = lines[18].replace("Diamond Cry","Diamond Cry Eyes")
    i1 += 1
  if len(lines) > 30:
    lines[30] = lines[30].replace("Diamon Tshirt", "Diamond Tshirt")
    i2 += 1
  if len(lines) > 26:
    lines[26] = lines[26].replace("Gold Diamon", "Gold Diamond")
    i3 += 1

  line = "".join(lines)
  if "Crown" in line or "Gold Diamond" in line or "Diamond Tshirt" in line:
    gold_cnt += 1
    cnt = gold_cnt
    fname = base + "/" + newdir + "/" + str(gold_cnt) + ".json"
  elif "Diamond Cry Eyes" in line or "Diamond Eyes" in line or \
     "Diamond Head"   in line:
    og_cnt += 1
    cnt = og_cnt
    fname = base + "/" + newdir + "/" + str(og_cnt) + ".json"
  else:
    reg_cnt += 1
    cnt = reg_cnt
    fname = base + "/" + newdir + "/" + str(reg_cnt) + ".json"
  # end if/elifs/else

  lines[1] = lines[1].split("#")[0] + "#" + str(cnt) + '",\n'
  line = "".join(lines)

  print(line)
  print("fname: ", fname)
  print("ii: ", ii)

  if ("Diamon" in line or "Daimon" in line or ("Gol" in line and "Gold Teeth" not in line and '"Gold"' not in line) or "Crown" in line) and cnt > 450+55:
    input(">>")

  with open(fname, "w") as fid:
    fid.write(line)
  # end with open
# end for ii
print("gold_cnt: ", gold_cnt)
print("og_cnt: ", og_cnt)
print("reg_cnt: ", reg_cnt)
print("i1: ", i1)
print("i2: ", i2)
print("i3: ", i3)
## end modify_metadata.py
