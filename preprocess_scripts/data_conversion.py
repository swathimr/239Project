import csv
import json
from collections import defaultdict

csvfile = open('careview.csv', 'r')
jsonfile = open('file.json', 'w',16777216)

delimiter = ','
result = {}

fieldnames = ("UserName","Rating","Movie")
projects = defaultdict(dict)
reader = csv.DictReader(csvfile,fieldnames)
for rowdict in reader:
     if None in rowdict:
      del rowdict[None]
     if(~projects.__contains__(rowdict.get('UserName'))):
                brand = rowdict.pop("UserName")
                product = rowdict.pop("Movie")
                projects[brand][product] = float(rowdict.get('Rating'))
               # print(dict(projects))

json.dump(dict(projects),jsonfile)
jsonfile.write('\n')