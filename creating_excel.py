import pandas as pd
import json
import glob
import os

##the entries which are available:
entries = ["country", "city", "day", "long", "lat", "nThumbsUp", "magvar",
           "subtype", "reportRating", "confidence", "reliability",
           "reportDescription", "roadType", "type", "uuid", "pubMillis", "street"]

df = pd.DataFrame(columns=entries)
print(df.head())
set_uuid = set()
counter = 0


for f in glob.glob("1/**/*.json"):

    g = f.split('\\')
    #g[1] is the day

    f = open(f, encoding="utf8")

    file = json.load(f)

    for i in file['alerts']:
        i['day'] = g[1]
        i['long'] = i['location']['x']
        i['lat'] = i['location']['y']
        # del i['location']
        counter = counter + 1
        if i["uuid"] not in set_uuid and i["type"] == "ACCIDENT":
            set_uuid.add(i["uuid"])
            df = df.append(i, ignore_index=True)

print(df.head())
print(len(df.index))

df.to_excel('Jan2021.xlsx', sheet_name='Sheet1')
