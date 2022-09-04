## just loads data to check leaderboards
import os
import ast
import glob
import numpy as np

home = os.getcwd()

## initialize storage dictionaries
stream_data = {
            "tweet_ids": np.array([]),
            "tuids": np.array([]),
            "usernames": np.array([]),
            "dates": np.array([]),
            "dates_s": np.array([]),
            "etypes": np.array([]),
            "texts": np.array([])
        }

keywords_data = {
            "dates":     [],
            "dates_s":   [],
            "tweet_ids": [],
            "tuids":     [],
            "usernames": [],
            "texts":     [],
            "ii": 0
        }

user_dict = {"discordId_to_username":{}, "linked_usernames":[]}

with open("data_big/linked.txt", "r") as fid:
    line = fid.read()
# end with
user_dict = ast.literal_eval(line)

S_PER_MINUTE = 60
S_PER_HOUR   = S_PER_MINUTE * 60
S_PER_DAY    = S_PER_HOUR   * 24
S_PER_MONTH  = S_PER_DAY    * 31
S_PER_YEAR   = S_PER_MONTH  * 12

def convert_sntime(sntime):
    if len(sntime.split(",")) == 6:
        yy,mm,dd,HH,MM,SS = sntime.split(", ")
    else:
        yy,mm,dd,HH,MM    = sntime.split(", ")
        SS = "00"
    # end if/else
    sntime = yy + "-" + mm.zfill(2) + "-" + dd.zfill(2) + "T" + HH.zfill(2) + ":" + MM.zfill(2) + ":" + SS.zfill(2) + ".000Z"
    return sntime
# end convert_sntime

def get_tweet_time_s(tweet_time):
    try:
        yy,mo,dd = tweet_time.split("-")
    except:
        print("tweet_time: ", tweet_time)
        raise
    # end try/except
    dd,hh         = dd.split("T")
    hh,mi,ss = hh.split(":")
    ss = ss[:-1]
    tweet_time_s = float(yy)*S_PER_YEAR   + float(mo)*S_PER_MONTH + \
                   float(dd)*S_PER_DAY    + float(hh)*S_PER_HOUR  + \
                   float(mi)*S_PER_MINUTE + float(ss)
    return tweet_time_s
# end get_tweet_time_s

## first keyword data
print("first do empty lists then confirm filler data produces same result")
fs = np.sort(glob.glob("data_big/keywords_data/keywords*.txt"))
for fn in fs:
    with open(fn, "r") as fid:
        line = fid.read()
    # end with

    tweets = line.split("Tweet(")[1:]
    nt = len(tweets)

    for ii in range(nt):
        tweet = tweets[ii]
        if ii % 1000 == 0 and ii != 0:
            print("ii: ", ii)
        # end if

        tweet_id = tweet.split("/status/")[1].split("'")[0]
        if tweet_id in keywords_data["tweet_ids"]:
            continue
        # end if
        if len(stream_data["tweet_ids"]) != 0:
            if tweet_id in stream_data["tweet_ids"]:
                continue
            # end if
        # end if

        date = convert_sntime(tweet.split("date=datetime.datetime(")[1].split(", tzinfo=")[0])
        date_s = str(get_tweet_time_s(date))

        tuid  = tweet.split("user=User(")[1].split("id=")[1].split(",")[0]
        uname = tweet.split("user=User(")[1].split("username='")[1].split(",")[0][:-1].lower()
        text  = tweet.split("content=")[1][1:].split(",")[0][:-1]

        keywords_data["tweet_ids"].append(tweet_id)
        keywords_data[    "dates"].append(date)
        keywords_data[  "dates_s"].append(date_s)
        keywords_data[    "tuids"].append(tuid)
        keywords_data["usernames"].append(uname)
        keywords_data[    "texts"].append(text)

        keywords_data["ii"] += 1
    # end for tweets
# end for fs
print("keywords_data ii: ", keywords_data["ii"])

DEFAULT_METHOD = "Points"
DEFAULT_STARTT = "2020-05-04T23:59:59.000Z"
DEFAULT_ENDT   = "4022-05-04T23:59:59.000Z"
DEFAULT_TIMEST = "all"
def get_rankings(method = DEFAULT_METHOD,
                            start_time = DEFAULT_STARTT, 
                            end_time   = DEFAULT_ENDT, 
                            time_str   = DEFAULT_TIMEST):
    print("begin get_rankins")

    start_time = get_tweet_time_s(start_time)
    end_time   = get_tweet_time_s(  end_time)

    weli = 0; wert = 0; werp = 0; weqt = 0; wkey = 0; wsrt = 0; wske = 0; wsqt = 0
    if method == "Likes":
        weli = 1
        etype = method.lower()
    elif method == "Retweets":
        # engagement retweets + stream retweets
        wert = 1; wsrt = 1
    elif method == "Tweets":
        # engagement replies, quotes + keywords + stream (except retweets)
        werp = 1; weqt = 1; wkey = 1; wske = 1; wsqt = 1
    elif method == "Points":
        print("in Points method")
        # engagement likes, RTs, replies, quotes + keywords + stream
        weli = 1; wert = 2; werp = 3; weqt = 5; wkey = 3; wsrt = 2; wske = 3; wsqt = 5
    # end if/elifs
    
    key = "tuids"
    tuids = wkey*[         keywords_data[key]]

    key = "usernames"
    usernames = wkey*[         keywords_data[key]]

    key = "dates_s"
    ky2 = "tuids"
    date_s0 = get_tweet_time_s("4000-01-01T00:00:00.000Z")
    dates_s = wkey*[         keywords_data[key]]

    tuids     = np.concatenate(tuids)
    dates_s   = np.concatenate(dates_s).astype(float)
    usernames = np.concatenate(usernames)

    junk, indsSU, junk = np.intersect1d(usernames, user_dict["linked_usernames"], 
                                        return_indices=True)

    print("shape dates_s: ", dates_s.shape)
    print("dates_s: ", dates_s)
    #indsB = np.where(dates_s[indsSU] >= start_time)
    #indsE = np.where(dates_s[indsSU][indsB] <= end_time)
    indsB = np.where(dates_s >= start_time)
    indsE = np.where(dates_s[indsB] <= end_time)
    
    print("tuids shape1: ", tuids.shape)
    #tuids = tuids[indsSU][indsB][indsE]
    tuids = tuids[indsB][indsE]
    print("tuids shape2: ", tuids.shape)
    tuids, indsU, vals = np.unique(tuids, return_index=True, return_counts=True)
    inds = np.argsort(vals)[::-1]

    if len(vals) == 0:
        vals = np.zeros(len(usernames))
        usernames = np.array(["anon"]*len(usernames))
    else:
        vals = vals[inds]
        #usernames = usernames[indsSU][indsB][indsE][indsU][inds]
        usernames = usernames[indsB][indsE][indsU][inds]
    # end if/else

    print("finished with get_rankings")
    return [vals, usernames]
# end get_rankings
vals, usernames = get_rankings()
print("got rankings!")

print("vals: ", vals)
print("usernames: ", usernames)

print("len vals: ", len(vals))
print("len usernames: ", len(usernames))

inds = np.where(usernames == "pokerface_gg")
uname = usernames[inds]
val = vals[inds]

print("uname; ", uname)
print("val: ", val)

print("success!")

## stream data
'''
stream_data = {
            "tweet_ids": np.array([]),
            "tuids": np.array([]),
            "usernames": np.array([]),
            "dates": np.array([]),
            "dates_s": np.array([]),
            "etypes": np.array([]),
            "texts": np.array([])
        }
fs = np.sort(glob.glob("stream_data?.txt"))
for fn in fs:
    with open(fn, "r") as fid:
        line = ast.literal_eval(line.replace("\n",""))
'''