import mysql.connector
import json

config = {
  'user': 'itravel',
  'password': 'itravel239',
  'host': 'recommendation-sys-instance.crkzapp5yylv.us-west-1.rds.amazonaws.com',
  'database': 'itravel',
  'raise_on_warnings': True,
}
db = mysql.connector.connect(**config)
#db = mysql.connector.connect(user="root", host ="localhost", database="test")
print "connection successful"
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version  : %s " % data
cursor.execute("DROP TABLE IF EXISTS USER")
sql = "CREATE TABLE USER (USER_ID CHAR(100) NOT NULL ,USER_NAME  CHAR(100))"
cursor.execute(sql)

with open('/Users/Shivani/Desktop/MS/MSSESem3/CMPE239/project/user.json') as data_file:    
    json_data = json.load(data_file)


count=len(json_data["data"])
print count
insert_user = ("INSERT INTO USER (USER_ID,USER_NAME) VALUES (%(u_id)s,%(u_name)s)")
for i in range(count):
    u_id= json_data["data"][i]["user_id"]
    u_name=json_data["data"][i]["name"]
    print u_id + u_name + str(i)
    insert_data = {
                  'u_id' : u_id,
                  'u_name':u_name
                  }
    cursor.execute(insert_user,insert_data)
    db.commit()
#print json_data["data"][1]["user_id"]
db.close()

