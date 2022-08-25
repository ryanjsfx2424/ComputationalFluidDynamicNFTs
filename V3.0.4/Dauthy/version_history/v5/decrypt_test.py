import os
from cryptography.fernet import Fernet

fernet = Fernet(os.environ["dauthyFern1"] + os.environ["dauthyFern2"] + os.environ["dauthyFern3"])

def decrypt(fname):
  with open(fname, "rb") as fid:
    line = fernet.decrypt(fid.read()).decode("utf-8")
  # end with
  return line
# end decrypt

hi_text = decrypt("EncryptTest0.txt")
go_text = decrypt("EncryptTest1.txt")
jo_text = decrypt("EncryptTest2.txt")
print("hi_text: ", hi_text)
print("go_text: ", go_text)
print("jo_text: ", jo_text)
