import ast
import requests
import numpy as np

TW_BT  = "AAAAAAAAAAAAAAAAAAAAA"
TW_BT += "ErfbQEAAAAAFbx63%2BKXNHraaXJh9Fp7rNwiU1s%"
TW_BT += "3D9sQ936aDcwyEmBuSrIuSMbmp5SBzWP4V4aoQgYy30eejRyvL9b"

headers = {
    'Authorization': f"Bearer {TW_BT}",
}

url_base = "https://api.twitter.com/2/tweets/search/stream"
url = url_base + "?user.fields=username&expansions=author_id" \
           + "&tweet.fields=created_at,public_metrics"
def connect_stream():
    print("1")
    print("2")
    cnt = 0
    wcnt = 0
    old_num = 0
    num = 0

    while True:
      wcnt += 1
      if wcnt >= 100:
        print("100 errors! exiting")
        return
      # end if
      print("wcnt: ", wcnt)
      try:
        s = requests.Session()
        with s.get(url, headers=headers, stream=True) as resp:
          print("3")
          for line in resp.iter_lines():
            print("4")
            if line:
              cnt += 1
              print("5")
              num = int(np.ceil(cnt / 100)) % 10
              if num != old_num:
                mode = "w"
                old_num = num
              # end if
              with open("stream_data" + str(num) + ".txt", mode) as fid:
                mode = "a"
                print("6")
                fid.write(line.decode("utf-8") + "\n")
                print("7")
              # end with open
            # end if
          # end for
        # end with
      except Exception as err:
        print("err4: ", err)
        print("err4 args: ", err.args[:])
      # end try/except
      print("outside try/except")
    # end while


keyword_query  = "(Rooty Roo OR Rooty Woo OR rootywoo OR Roo Troop OR rootroop"
keyword_query += " OR rootroops OR tree roo OR roo bounty OR roo bounties"
keyword_query += " OR rootyroo OR RootyRoo OR rootroopnft OR troopsales)"
#keyword_query += " OR \uD83C\uDF33\uD83E\uDD98)"
keyword_query += " OR (@rootroopnft OR @troopsales)"
retweet_rule = "(retweets_of:rootroopnft OR retweets_of:troopsales)"
#quote_rule = "(to:rootroopnft OR to:troopsales) is:quote"
quote_rule = '(url:"twitter.com/rootroopnft/status" OR "url:twitter.com/troopsales/status") is:quote'

def add_rules():
  json_data = {
               "add": [
                       {"value": keyword_query, "tag": "keywordstag"},
                       {"value": retweet_rule,  "tag": "retweetstag"},
                       {"value": quote_rule,  "tag": "quotestag"}
                      ]
              }

  response = requests.post(url_base + "/rules", headers=headers, json=json_data)
  print(response)
  print(response.text)

def get_rules_ids():
  print("begin get_rules_ids")
  ids = []
  response = requests.get(url_base + "/rules", headers=headers)
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

def delete_rules(ids):
  print("begin delete_rules")
  json_data = {"delete": {"ids":ids}}
  response = requests.post(url_base + "/rules", headers=headers, json=json_data)
  print(response)
  print(response.text)
# end delete_rules

print("8")
ids = get_rules_ids()
delete_rules(ids)
add_rules()
connect_stream()
print("9")
