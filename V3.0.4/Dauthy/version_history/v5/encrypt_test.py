import os
from cryptography.fernet import Fernet

to_save = ["hi", "go", "jo"]
fernet = Fernet(os.environ["dauthyFern1"] + os.environ["dauthyFern2"] + os.environ["dauthyFern3"])

for ii,el in enumerate(to_save):
  with open("EncryptTest" + str(ii) + ".txt", "wb") as fid:
    print("el: ", el)
    fid.write(fernet.encrypt( (str(el)).encode("utf-8") ))
  # end with
# end for
