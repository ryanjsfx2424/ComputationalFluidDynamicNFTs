import os
import time

fname = "running_processes.txt"
dcnt = 0
while True:
  os.system("ps aux | grep python > " + fname)

  with open(fname, "r") as fid:
    line = fid.read()
  # end with

  if "tweeteroo_bf.py" not in line:
    print("tweeteroo bf not running?")

  if "ScrapeTweets_server.py" not in line:
    print("Tweeteroo not running?")

  if " dauthy.py" not in line:
    print("dauthy not running?")
    dcnt += 1
    result = os.system("nohup python3 -u dauthy.py > logfile" + str(dcnt) + ".txt 2>&1 &")
    print("result: ", result)
  # end if

  time.sleep(5)
# end while
