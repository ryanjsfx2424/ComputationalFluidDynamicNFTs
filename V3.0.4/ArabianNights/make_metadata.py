with open("metadata/0", "r") as fid:
  lines = fid.readlines()
# end with

for ii in range(1,666):
  newlines = lines + []
  with open("metadata/" + str(ii), "w") as fid:
    newlines[1] = newlines[1].replace("#1", "#" + str(ii+1))
    newlines[3] = newlines[3].replace("1.png", str(ii+1) + ".png")
    newlines[7] = newlines[7].replace("1", str(ii+1))
    for line in newlines:
      fid.write(line)
    # end for
  # end with
# end for
