# Python program to read
# json file

import json

json_from_filepath = "c:\\tweets\\tweets.log"
json_to_filepath = "c:\\tweets\\tweets_to.json"

f = open(json_from_filepath ,'r', encoding="utf8")

# returns JSON object as
# a dictionary
data = json.load(f)

#add missing field
for d in data : 
    d["lang"]="en"
    d['id'] = d.pop('tweet_id')
    del d["tweet_coord"]


with open(json_to_filepath, 'w') as t:
    t.write('\n'.join(map(json.dumps, data)))
    
    
f.close()
t.close()
