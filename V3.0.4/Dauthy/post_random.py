## post_random.py by TheLunaLabs
"""
The purpose of this script is to post a random hash to
a webpage that will be used to authenticate users.
"""
import os
import time
from cryptography.fernet import Fernet
from flask import Flask, render_template
app = Flask(__name__)
#fern = Fernet.generate_key()
#print(fern)
fern = Fernet(os.environ["dwEncKey"])

app.debug = True
@app.route("/")
def post_random():
  with open("authentication_token.enc", "rb") as fid:
    token = fern.decrypt(fid.read())
  # end with open
  token = str(token)[2:-1]
  print(token)
  return render_template("token.html", token=token)

if __name__ == "__main__":
  from url_police import AuthenticationDiscordBot
  auth = AuthenticationDiscordBot()
  auth.get_random()
  app.run()
