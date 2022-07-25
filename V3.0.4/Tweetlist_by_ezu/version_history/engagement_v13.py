import os
import yt
import ast
import time
from ezu_tweeteroo import *
yt.enable_parallelism()
class Engagement(EzuTweeteroo):
    def __init__(self):
        self.init_auth()
        self.init_keywords()

        self.CURL_BASE = "curl --request GET --url '"
        self.CURL_HEADER = "' --header 'Authorization: Bearer "
        self.TWITTER_API_BASE = "https://api.twitter.com/2/tweets/"

        self.LONG_SLEEP  = 60.1
        self.QUICK_SLEEP =  0.1
    # end __init__

    def get_project_tweet_ids(self):
        with open(self.fname_project_tweet_ids, "r") as fid:
            tweet_ids = ast.literal_eval(fid.read())
        # end with
        return tweet_ids
    # end get_project_tweet_ids
    
    def scrape_engagement(self):
        wcnt = 0
        while True:
            print("wcnt se25: ", wcnt)
            wcnt += 1
            tweet_ids = self.get_project_tweet_ids()

            for tweet_id in tweet_ids:
                print("tweet_id: ", [tweet_id])
                for etype in yt.parallel_objects(["likes", "retweets", "quotes"]):
                    print("etype: ", etype)
                    scraped = self.get_engagement(tweet_id, etype)
                    if scraped:
                        time.sleep(self.LONG_SLEEP)
                    # end if
                # end for etype
            # end for project_tweet_ids
        # end while True
    # end scrape_engagement

    def get_engagement(self, tweet_id, etype):
        print("BEGIN get_engagement for etype, tweet_id: ", etype, tweet_id)
        #input(">>")
        url  = self.TWITTER_API_BASE
        url += tweet_id # not for replies tho
        nl = 4
        if   etype == "likes":
            url += "/liking_users?"
        elif etype == "retweets":
            url += "/retweeted_by?"
        elif etype == "quotes":
            nl = 6
            url += "/quote_tweets?expansions=author_id&"
        # end if/elifs
        url += "user.fields=username&max_results=100&tweet.fields=public_metrics"
        url_og = url + ""

        lines = []
        token = ""
        fname = "data_big/" + etype + "/activity_" + self.PROJECT_TWITTER + "_" + tweet_id + ".txt"
        if os.path.exists(fname) and os.stat(fname).st_size != 0:
            with open(fname, "r") as fid:
                lines = fid.readlines()
                last_lines = lines[-nl:]
                token = last_lines[0]
                token = token.split("next_token: ")[1]
                token = token.replace(" ","").replace("\n","")
                if token == "None":
                    lines = lines[:-nl]
                    last_lines = lines[-nl:]
                    token = last_lines[0]
                    token = token.split("next_token: ")[1]
                    token = token.replace(" ","").replace("\n","")
                # end if
            # end with
        # end if

        wcnt = 0
        while token != "None":
            wcnt += 1; print("wcnt ge80: ", wcnt)
            if token != "":
                url = url_og + "&pagination_token=" + token
            # end if
      
            cmd = self.CURL_BASE + url + self.CURL_HEADER + self.auth + "' > " + fname + "_"
            print("\n\ncmd: ", cmd)
            result = os.system(cmd)
            #input(">>")

            if result != 0:
                print("error during curl, lost wifi?")
                time.sleep(self.LONG_SLEEP)
                continue
            # end if

            with open(fname + "_", "r") as fid:
                line = fid.read()
            # end with open
            line = ast.literal_eval(line)

            next_token = "None"
            if "next_token" in line["meta"]:
                next_token = line["meta"]["next_token"]
            # end if

            if str(line["meta"]["result_count"]) == str(0):
                print("result count zero")
                with open(fname, "w") as fid:
                    for ll in lines:
                        if ll[-1] != "\n":
                            ll += "\n"
                        # end if
                        fid.write(ll)
                    # end for
                    fid.write("next_token: " + next_token + "\n")
                    fid.write("results_count: " + str(line["meta"]["result_count"]) + "\n")
                    fid.write("twitter_ids: "       + str(twids ) + "\n")
                    if etype != "quotes":
                        fid.write("twitter_usernames: " + str(unames))
                    else:
                        fid.write("twitter_usernames: " + str(unames) + "\n")
                        fid.write("tweet_ids: "         + str(tweds ) + "\n")
                        fid.write("texts: "             + str(texts))
                    # end if/else
                    return True
                # end with
            # end if

            if etype != "quotes":
                twids  = []
                unames = []

                for ii in range(len(line["data"])):
                    twids.append( line["data"][ii]["id"])
                    unames.append(line["data"][ii]["username"])
                # end for ii

                new_lines = ["next_token: " + next_token + "\n",
                             "results_count: "     + str(line["meta"]["result_count"]) + "\n",
                             "twitter_ids: "       + str(twids ) + "\n",
                             "twitter_usernames: " + str(unames)
                            ]
            else:
                twids  = []
                unames = []
                tweds  = [] # tweet's id
                texts  = []

                for ii in range(len(line["includes"]["users"])):
                    twids.append( line["includes"]["users"][ii]["id"])
                    unames.append(line["includes"]["users"][ii]["username"])
                # end for ii

                # next grab tweet id and texts from data
                for ii in range(len(line["data"])):
                    tweds.append(line["data"][ii]["id"])
                    texts.append(line["data"][ii]["text"])
                # end for ii

                new_lines = ["next_token: " + next_token + "\n",
                             "results_count: "     + str(line["meta"]["result_count"]) + "\n",
                             "twitter_ids: "       + str(twids ) + "\n",
                             "twitter_usernames: " + str(unames) + "\n",
                             "tweet_ids: "         + str(tweds ) + "\n",
                             "texts: "             + str(texts )
                            ]
            # end if/else
            
            with open(fname, "w") as fid:
                for ll in lines:
                    if ll[-1] != "\n":
                        ll += "\n"
                    # end if
                    fid.write(ll)
                # end for
                
                for ll in new_lines:
                    fid.write(ll)
                # end for
            # end with open
            lines = lines + new_lines
            print("token old: ", [token])
            print("next_token: ", [next_token])
            token = next_token + ""

            if "None" not in token:
                print("188about to sleep a minute")
                time.sleep(self.LONG_SLEEP)
            # end if
        # end while
        if wcnt == 0:
            return False
        # end if

        print("SUCCESS get_engagement for etype, tweet_id: ", etype, tweet_id)
        return True
    # end get_engagement
# end Engagement
if __name__ == "__main__":
    ee = Engagement()
    ee.scrape_engagement()
# end if
## end engagement.py