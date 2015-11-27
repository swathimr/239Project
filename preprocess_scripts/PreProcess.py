import json

data = []
fo = open('write.txt', 'a',16777216)

# Parses business json data (business id,address,longitude,latitude,star)
with open('business.json') as f:
    for line in f:
        val = str(json.loads(line)["business_id"])+","+str(json.loads(line)["stars"])+","+str(json.loads(line)["longitude"])+","+str(json.loads(line)["latitude"])+","+str(json.loads(line)["full_address"]).replace('\n','')
        fo.write(val+"\n")

fo.close()

# Parses review json file and creates csv file
with open('review.json') as f:
    for line in f:
        val = str(json.loads(line)["user_id"])+","+str(json.loads(line)["business_id"])+","+str(json.loads(line)["stars"])
        fo.write(val+"\n")


