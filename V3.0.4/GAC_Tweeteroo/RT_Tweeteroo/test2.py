def safe_load_abu():
    abu = {}

    data_dir = "twitter_data"

    os.chdir(data_dir + "/user_data3")
    fs = glob.glob("*.json")
    for fn in fs:
      with open(fn, "r") as fid:
        if fn[0].isdigit():
          abu[fn.replace(".json","")] =  ast.literal_eval(fid.read())
        else:
          if "latest_tweet_time_s.json" == fn:
            abu[fn.replace(".json","")] =  float(fid.read())
          else:
            abu[fn.replace(".json","")] =  str(fid.read())
      # end with
    # end for
    os.chdir("../..")
    return abu
  # end safe_load_abu

abu = safe_load_abu()

for key in abu:
    if "ParentingAces" in abu[key]["usernames"]:
        userid = key
        break
# end for

