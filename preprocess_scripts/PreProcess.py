import json,csv

data = []
fo = open('write.txt', 'a',16777216)

#business script(business id,address,longitude,latitude,star)
with open('business.json') as f:
    for line in f:
        if str(json.loads(line)["state"])=='CA':
            val = str(json.loads(line)["business_id"])+","+str(json.loads(line)["stars"])+","+str(json.loads(line)["longitude"])+","+str(json.loads(line)["latitude"])+","+str(json.loads(line)["full_address"]).replace('\n','').replace(',','')
            fo.write(val+"\n")



#review script
with open('review.json') as f:
    for line in f:
        #data.append(json.loads(line))
        #print json.loads(line)["user_id"]+","+json.loads(line)["stars"]
        val = str(json.loads(line)["user_id"])+","+str(json.loads(line)["stars"])+","+str(json.loads(line)["business_id"])
        fo.write(val+"\n")

# Extracting only CA location data
dict={}
dict.clear()

with open('cabusiness.csv', 'rt') as f:
     reader = csv.reader(f, delimiter=',')
     for row in reader:
        dict[row[0]]=row[1]

with open('review.json') as f:
    for line in f:
        businessid=str(json.loads(line)["business_id"])
        if dict.has_key(businessid):
            val = str(json.loads(line)["user_id"])+","+str(json.loads(line)["stars"])+","+str(json.loads(line)["business_id"])
            fo.write(val+"\n")
    fo.close()