import os
import ast
import glob


os.system("mkdir -p user_dataL3")
os.system("mkdir -p user_dataL")

with open("../discord_data/linked_1.json", "r") as fid:
  line = fid.read()
# end with
line = ast.literal_eval(line)

linked_userids = []
for el in line:
  linked_userids.append(el["id_str"])
# end for

with open("activity_by_user3.json", "r") as fid:
  line = ast.literal_eval(fid.read())
# end with open

os.chdir("user_dataL3")
for userid in line:
  if userid not in linked_userids:
    continue
  if userid[0].isdigit():
    with open(str(userid) + ".json", "w") as fid:
      fid.write(str(line[userid]))
    # end with
  # end if
# end for
os.chdir("..")

with open("activity_by_user.json", "r") as fid:
  line = ast.literal_eval(fid.read())
# end with open

os.chdir("user_dataL")
for userid in line:
  if userid not in linked_userids:
    continue
  if userid[0].isdigit():
    with open(str(userid) + ".json", "w") as fid:
      fid.write(str(line[userid]))
    # end with
  # end if
# end for
