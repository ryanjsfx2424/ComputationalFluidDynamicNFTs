import time
import datetime
import numpy as np
from flask     import Flask
from threading import Thread
start = time.time()
update_dts = []
update_time = time.time()

app = Flask("")

@app.route("/")
def home():
  global update_time
  print("1: ", update_dts)
  print("2: ", start)
  print("3: ", update_time)
  update_dts.append(time.time() - update_time)
  update_time = time.time()

  now = datetime.datetime.today()
  now = str(now.year) + "-" + str(now.month)  + "-" + str(now.day) + " " + \
        str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)

  text  = "I've been running for " + str(time.time()-start) + " seconds"
  text += "\nLast updated: " + now
  text += "\nMaximum time (in seconds) between updates: " + \
          str(np.max(np.array(update_dts)))

  return text
# end def home

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
