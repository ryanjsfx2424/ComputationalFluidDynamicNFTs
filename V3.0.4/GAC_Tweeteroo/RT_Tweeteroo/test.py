import ast
import glob

fs = glob.glob("stream_data?.txt")
for fn in fs:
  print("fn: ", fn)
  with open(fn, "r") as fid:
    for line in fid:
      print("line: ", line)
      line = ast.literal_eval(line)    
      print("loaded!")
