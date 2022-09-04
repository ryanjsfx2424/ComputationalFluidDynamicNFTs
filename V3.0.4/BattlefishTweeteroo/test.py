## just loads data to check leaderboards
import os
import ast
import glob
import json
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

CHUNK_SIZE = 1000
nfs = len(glob.glob("data_big/keywords_data/keywords*.txt"))
num = 2 * CHUNK_SIZE * nfs

filler_date = ["XXXX-XX-XXTXX:XX:XX.XXXZ"]
filler_text = [280*"X"]

keywords_data = {
    "dates":     np.array(num*filler_date),
    "dates_s":   np.array(num*filler_date),
    "tweet_ids": np.array(num*filler_date),
    "tuids":     np.array(num*filler_date),
    "usernames": np.array(num*filler_date),
    "texts":     np.array(num*filler_text),
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

FLAG_KEY = "keywords"
FLAG_RTS = "retweets"
FLAG_QTS = "quotes"

PROJECT_TWITTER = "BattleFish_"

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

        ind = keywords_data["ii"]
        # keywords_data["tweet_ids"].append(tweet_id)
        # keywords_data[    "dates"].append(date)
        # keywords_data[  "dates_s"].append(date_s)
        # keywords_data[    "tuids"].append(tuid)
        # keywords_data["usernames"].append(uname)
        # keywords_data[    "texts"].append(text)
        keywords_data["tweet_ids"][ind] = tweet_id
        keywords_data[    "dates"][ind] = date
        keywords_data[  "dates_s"][ind] = date_s
        keywords_data[    "tuids"][ind] = tuid
        keywords_data["usernames"][ind] = uname
        keywords_data[    "texts"][ind] = text

        keywords_data["ii"] += 1
    # end for tweets
# end for fs
print("keywords_data ii: ", keywords_data["ii"])

inds = np.where(keywords_data["dates"] != filler_date)
keywords_data["dates"    ] = keywords_data["dates"    ][inds]
keywords_data["dates_s"  ] = keywords_data["dates_s"  ][inds]
keywords_data["tweet_ids"] = keywords_data["tweet_ids"][inds]
keywords_data[    "tuids"] = keywords_data[    "tuids"][inds]
keywords_data["usernames"] = keywords_data["usernames"][inds]
keywords_data[    "texts"] = keywords_data[    "texts"][inds]

# next, let's do stream data
fs = np.sort(glob.glob("data_big/stream/stream_data?.txt"))
for fn in fs:
    print("fn: ", fn)
    with open(fn, "r") as fid:
        for line in fid:
            line = ast.literal_eval(line.replace("\n",""))

            if "matching_rules" not in line:
                print("1287 cont")
                continue
            # end if

            if not ("data" in line and    
                (     "id" in line["data"] and 
                    "text" in line["data"] and 
              "created_at" in line["data"])) or \
        not (   "includes" in line and "users" in line["includes"]):
                print("stuff not in line")
                input(">>")
                continue
            # end if

            tweet_id = line["data"]["id"]
            tuid     = line["data"]["author_id"]
            text     = line["data"]["text"].lower()
            date     = line["data"]["created_at"]
            date_s   = str(get_tweet_time_s(date))

            flag = "keywords"
            flag = FLAG_KEY
            for matching_rule in line["matching_rules"]:
                if   PROJECT_TWITTER + "_retweetstag" in matching_rule["tag"]:
                    flag = FLAG_RTS
                    text = text[:2]
                elif PROJECT_TWITTER + "_quotestag" in matching_rule["tag"]:
                    flag = FLAG_QTS
                # end if/elif
            # end for

            if flag != FLAG_RTS:
                if tweet_id in stream_data["tweet_ids"]:
                    continue
                # end if
            else:
                inds = np.where(stream_data["tuids"] == tuid)
                if tweet_id in stream_data["tweet_ids"][inds]:
                    continue
                # end if
            # end if/else

            for user in line["includes"]["users"]:
                if user["id"] == tuid:
                    username = user["username"].lower()
                    break
                # end if
            # end for

            stream_data["tweet_ids"  ] = np.append(stream_data["tweet_ids"  ], tweet_id)
            stream_data[    "tuids"  ] = np.append(stream_data[    "tuids"  ], tuid)
            stream_data["usernames"  ] = np.append(stream_data["usernames"  ], username)
            stream_data[    "dates"  ] = np.append(stream_data[    "dates"  ], date)
            stream_data[    "dates_s"] = np.append(stream_data[    "dates_s"], date_s)
            stream_data[   "etypes"  ] = np.append(stream_data[   "etypes"  ], flag)
            stream_data[    "texts"  ] = np.append(stream_data[    "texts"  ], text)
            print("1343 added to stream data! uname, tweet_id: ", tweet_id, username)
        # end for line in fid
    # end with open
# end for fn in fs

with open("data_big/stream/stream.txt", "w") as fid:
    fid.write(json.dumps(list(stream_data["tweet_ids"])) + "\n")
    fid.write(json.dumps(list(stream_data["tuids"    ])) + "\n")
    fid.write(json.dumps(list(stream_data["usernames"])) + "\n")
    fid.write(json.dumps(list(stream_data["dates"    ])) + "\n")
    fid.write(json.dumps(list(stream_data["dates_s"  ])) + "\n")
    fid.write(json.dumps(list(stream_data["etypes"   ])) + "\n")
    fid.write(json.dumps(list(stream_data["texts"    ])) + "\n")
# end with open

engagement = {}
for etype in ["likes", "retweets", "replies", "quotes"]:
    fnames = np.sort(glob.glob("data_big/" + etype + "/activity_*.txt"))
    tuids = []
    usernames = []
    tweet_ids = []
    
    for fname in fnames:
        usernames_f = []
        with open(fname, "r") as fid:
            for line in fid:
                if "next_token: " in line and "None" not in line:
                    next_token = line.split("next_token: ")[1]
                elif "twitter_ids: " in line and "[]" not in line:
                    tuids_line = line.replace("'", "").replace("[", "").replace("]","").replace("\n","").split("twitter_ids: ")[1]
                    if ", " in tuids_line:
                        tuids += tuids_line.split(", ")
                    else:
                        tuids += [tuids_line]
                    # end if/else
                elif "twitter_usernames: " in line and "[]" not in line:
                    usernames_line = line.replace("'", "").replace("[", "").replace("]","").replace("\n","").split("twitter_usernames: ")[1]
                    if ", " in usernames_line:
                        usernames += usernames_line.split(", ")
                        usernames_f += usernames_line.split(", ")
                    else:
                        usernames   += [usernames_line]
                        usernames_f += [usernames_line]
                    # end if/else
                # end if/elifs
            # end for line in fid
        # end with open
        if len(usernames) != len(tuids):
            print("usernames != tweet_ids ???")
            print("len usernames: ", len(usernames))
            print("len tuids: ", len(tuids))
            raise
        # end if
        #print("fname: ", fname)
        try:
            tweet_id = int(fname.split("activity_gac_")[1].split(".txt")[0])
        except:
            tweet_id = int(fname.split("activity_" + PROJECT_TWITTER + "_")[1].split(".txt")[0])
        tweet_ids += len(usernames_f)*[tweet_id]

        if len(usernames) != len(tuids):
            print("usernames != tweet_ids ???")
            print("len usernames: ", len(usernames))
            print("len tuids: ", len(tuids))
            raise
        # end if
    # end for fnames

    usernames = np.array(usernames)
    if len(usernames) != 0:
        usernames = np.char.lower(usernames)

    engagement[etype] = {
        "tweet_ids": np.array(tweet_ids),
        "tuids": np.array(tuids),
        "usernames": usernames
    }
# end for etypes
print("engagement: ", engagement)

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

    indsSRT = np.where(stream_data["etypes"] == FLAG_RTS)
    indsSKE = np.where(stream_data["etypes"] == FLAG_KEY)
    indsSQT = np.where(stream_data["etypes"] == FLAG_QTS)

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
    tuids = weli*[engagement[   "likes"][key]] \
            + wert*[engagement["retweets"][key]] \
            + werp*[engagement[ "replies"][key]] \
            + weqt*[engagement[  "quotes"][key]] \
            + wkey*[         keywords_data[key]] \
            + wsrt*[           stream_data[key][indsSRT]] \
            + wske*[           stream_data[key][indsSKE]] \
            + wsqt*[           stream_data[key][indsSQT]]

    key = "usernames"
    usernames = weli*[engagement[   "likes"][key]] \
            + wert*[engagement["retweets"][key]] \
            + werp*[engagement[ "replies"][key]] \
            + weqt*[engagement[  "quotes"][key]] \
            + wkey*[         keywords_data[key]] \
            + wsrt*[           stream_data[key][indsSRT]] \
            + wske*[           stream_data[key][indsSKE]] \
            + wsqt*[           stream_data[key][indsSQT]]

    key = "dates_s"
    if key in engagement["likes"]:
        dates_s = weli*[engagement[   "likes"][key]] \
                + wert*[engagement["retweets"][key]] \
                + werp*[engagement[ "replies"][key]] \
                + weqt*[engagement[  "quotes"][key]] \
                + wkey*[         keywords_data[key]] \
                + wsrt*[           stream_data[key][indsSRT]] \
                + wske*[           stream_data[key][indsSKE]] \
                + wsqt*[           stream_data[key][indsSQT]]
    else:
        ky2 = "tuids"
        date_s0 = get_tweet_time_s("4000-01-01T00:00:00.000Z")
        dates_s = weli*[np.zeros(len(engagement[   "likes"][ky2]))+date_s0] \
                + wert*[np.zeros(len(engagement["retweets"][ky2]))+date_s0] \
                + werp*[np.zeros(len(engagement[ "replies"][ky2]))+date_s0] \
                + weqt*[np.zeros(len(engagement[  "quotes"][ky2]))+date_s0] \
                + wkey*[         keywords_data[key]] \
                + wsrt*[           stream_data[key][indsSRT]] \
                + wske*[           stream_data[key][indsSKE]] \
                + wsqt*[           stream_data[key][indsSQT]]
    # end if/else
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