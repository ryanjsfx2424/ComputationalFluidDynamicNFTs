import ast
import time
import requests
import numpy as np
from tweeteroo_pn import *

MAX_LOOPS = 5

class Stream(Tweeteroo2):
  def __init__(self):
    self.init_auth()
    self.init_keywords()
    self.tweet_rule   =              "from:" + self.PROJECT_TWITTER
    self.retweet_rule =       "retweets_of:" + self.PROJECT_TWITTER
    self.quote_rule   = '(url:"twitter.com/' + self.PROJECT_TWITTER + '/status") is:quote'

    self.headers = {"Authorization": "Bearer " + self.auth}

    self.url_base = "https://api.twitter.com/2/tweets/search/stream"
    self.url = self.url_base + "?user.fields=username&expansions=author_id" \
                             + "&tweet.fields=created_at,public_metrics,conversation_id"
    self.start = time.time()
  # end __init__

  def add_rules(self):
    json_data = {
        "add": [
                {"value": self.keywords_help, "tag": self.PROJECT_TWITTER + "_keywordstag"},
                {"value": self.retweet_rule,   "tag": self.PROJECT_TWITTER + "_retweetstag"},
                {"value": self.quote_rule,     "tag": self.PROJECT_TWITTER + "_quotestag"},
                {"value": self.tweet_rule,     "tag": self.PROJECT_TWITTER + "_tweetstag"}
               ]
                }

    response = requests.post(self.url_base + "/rules", headers=self.headers, 
                             json=json_data)
    print(response)
    print(response.text)

  def get_rules_ids(self):
    print("begin get_rules_ids")
    ids = []
    response = requests.get(self.url_base + "/rules", headers=self.headers)

    print(response)
    print(response.text)

    text = ast.literal_eval(response.text)
    if "data" in list(text.keys()):
      data = text["data"]
      for val in data:
        ids.append(val["id"])
      # end for
      return ids
    # end if
  # end get_rules_ids

  def delete_rules(self, ids):
    print("begin delete_rules")
    json_data = {"delete": {"ids":ids}}
    response = requests.post(self.url_base + "/rules", 
                             headers=self.headers, json=json_data)
    print(response)
    print(response.text)
  # end delete_rules

  def connect_stream(self):
    print("1")
    print("2")
    cnt = 0
    wcnt = 0
    old_num = 0
    num = 0

    while True:
      wcnt += 1
      if wcnt >= MAX_LOOPS:
        print(str(MAX_LOOPS) + " errors! exiting")
        return
      # end if
      print("wcnt: ", wcnt)
      try:
        s = requests.Session()
        with s.get(self.url, headers=self.headers, stream=True) as resp:
          print("3")
          for line in resp.iter_lines():
            print("4")
            if time.time() - self.start > 3600:
              wcnt = 0
              self.start = time.time()
            if line:
              cnt += 1
              print("5")
              num = 11+int(np.ceil(cnt / int(1e6)))
              if num != old_num:
                mode = "w"
                old_num = num
              # end if
              with open("data_big/stream/stream_data" + str(num) + ".txt", mode) as fid:
                mode = "a"
                print("6")
                fid.write(line.decode("utf-8") + "\n")
                print("7")
              # end with open
            # end if
          # end for
        # end with
      except Exception as err:
        print("55 stream connect_stream err: ", err)
        print("56 scs err.args: ", err.args[:])
        if "Connection reset by peer" in err:
            print("going to try recursing")
            time.sleep(60.1)
            self.connect_stream()
            print("outside recurse")
            return
        # end if
      # end try/except
      print("outside try/except")
    # end while
  # end connect_stream
# end Stream

if __name__ == "__main__":
  st = Stream()

  ids = st.get_rules_ids()
  print("ids: ", ids)
  st.delete_rules(ids)
  st.add_rules()
  st.connect_stream()
# end if
## end stream.py
