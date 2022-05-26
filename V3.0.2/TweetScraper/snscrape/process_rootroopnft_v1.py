## process_rootroopnft.py

# first let's just check how many tweets it grabbed.
with open("rootroopnft.txt", "r") as fid:
  line = fid.read()
# end with open

line = line.split("Tweet(url=")
print("line[0]: ", line[0])
print("line[-1]: ", line[-1])

last_date = line[-1].split("date=datetime.datetime(")[1].split(", tzinfo=datetime.timezone.utc),")[0]
print("last_date: ", last_date) # returned 2021, 11, 23, 23, 32, 3 (also the oldest tweet I was able to fetch)

print("len line: ", len(line)) # returned 1484
