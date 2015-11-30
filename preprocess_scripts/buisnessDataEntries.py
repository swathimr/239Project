import mysql.connector
import csv

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

'''
cursor.execute("DROP TABLE IF EXISTS BUSINESS")
sql = "CREATE TABLE BUSINESS (B_ID CHAR(100) NOT NULL, RATING FLOAT(10,5), LONGITUDE DECIMAL(25,20), LATITUDE DECIMAL(25,20),ADDRESS CHAR(255), STATE CHAR(100))"
cursor.execute(sql)
csv_data = csv.reader(file('/Users/Shivani/Desktop/MS/MSSESem3/CMPE239/project/business.csv'))
insert_business = ("INSERT INTO BUSINESS (B_ID, RATING, LONGITUDE,LATITUDE,ADDRESS, STATE) VALUES (%s, %s, %s, %s, %s, %s)")
'''

cursor.execute("DROP TABLE IF EXISTS BUSINESS_CA")
sql = ("CREATE TABLE BUSINESS_CA (B_ID CHAR(100) NOT NULL, B_NAME CHAR(100), PHOTO_URL CHAR (255), RATING FLOAT(10,5), LONGITUDE DECIMAL(25,20), LATITUDE DECIMAL(25,20), ADDRESS CHAR(255))")
cursor.execute(sql)
#csv_data = csv.reader(open('/Users/Shivani/239Project/data/business_CA1.csv', 'rU'),dialect=csv.excel_tab)
#csv_data = csv.reader(file('/Users/Shivani/Desktop/MS/MSSESem3/CMPE239/project/business.csv'))
insert_business = "INSERT INTO BUSINESS_CA (B_ID, B_NAME, PHOTO_URL, RATING, LONGITUDE, LATITUDE, ADDRESS) VALUES (%s, %s, %s, %s, %s, %s, %s)"

with open('/Users/Shivani/239Project/data/business_CA1.csv', 'rU') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        print row
        print csvreader.line_num
        cursor.execute(insert_business,row)

'''for row in csv_data:
    print row
    print csv_data.line_num
    #cursor.execute(insert_business,row)'''

db.commit()
cursor.close()
db.close()