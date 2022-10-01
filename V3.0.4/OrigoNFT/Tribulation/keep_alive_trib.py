import os
import time

fname = "running_processes.txt"
dcnt = 0
while True:
  os.system("ps aux | grep node > " + fname)

  with open(fname, "r") as fid:
    line = fid.read()
  # end with

  if "tribulation.js" not in line:
    print("trib not running")
    dcnt += 1
    result = os.system("nohup node tribulation.js > logfile.txt" + str(dcnt) + ".txt 2>&1 &")
    print("result: ", result)
  # end if

  time.sleep(5)
# end while
