from flask import Flask,render_template,request
import functions,reviewdata
import mysql.connector

app = Flask(__name__)

# sql connection
config = {
  'user': 'itravel',
  'password': 'itravel239',
  'host': 'recommendation-sys-instance.crkzapp5yylv.us-west-1.rds.amazonaws.com',
  'database': 'itravel',
  'raise_on_warnings': True,
}
db = mysql.connector.connect(**config)
cursor = db.cursor()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello/')
def hello(name=None):
    return render_template('WelcomePage.html')

@app.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    _name = request.form['name']
    _email = request.form['email']
    _password = request.form['password']
   # session['username'] = request.form['name']

    #add user information into db

    print _email+"::"+_name+"::"+_password
    return render_template('UserHomePage.html',email=_email)

@app.route('/login',methods=['POST'])
def login():

    # read the posted values from the UI
    _email = request.form['email']
    _password = request.form['password']
    """check for user ifno in db
    if exists navigate to homwpage
    else stay in same page with proper error message"""
    print _email+"::"+_password
    return render_template('UserHomePage.html',email=_email)

@app.route('/ItemRecommend',methods=['GET'])
def Item_based():
    user_id="T9hGHsbJW9Hw1cJAlIAWmw"
    productData = functions.flipPersonToPlaces(reviewdata.reviews)

    #to do : get place name and pic to show in ui
    print "Finding similar Places "
    similar_item=functions.mostSimilar(productData,"4iTRjN_uAdAb7_YZDVHJdg")
    b_data=[]
    for bid in dict(similar_item).keys():
        print "bid::"+bid
        sql = ("SELECT B_NAME, PHOTO_URL from BUSINESS_CA where B_ID = '%s'" % bid)
        cursor.execute(sql)
        data = cursor.fetchone()
        print cursor._executed.decode("utf8")
        if data != None:
            b_data.append(data)
    print b_data

    print "Computing Item Similarity"
    itemSimilarity = functions.computeItemSimilarities(productData)

    print "Item Based Filtering for Recommendations"
    recommendedplc_ib=functions.itemBasedFiltering(reviewdata.reviews,user_id,itemSimilarity)
    print recommendedplc_ib.keys() #send to shivani
    locations =[]
    #sql = ("SELECT B_NAME, LATITUDE, LONGITUDE, RATING from BUSINESS_CA where B_ID = '%s'" % bid)
    sql = ("SELECT B_NAME, LATITUDE, LONGITUDE, RATING from BUSINESS_CA where B_ID = '81IjU5L-t-QQwsE38C63hQ'" )
    for bid in recommendedplc_ib.keys():
        cursor.execute(sql)
        data_map = cursor.fetchone()
        print cursor._executed.decode("utf8")
        print data_map
        locations.append(data_map) #swathi : locations contains the data you need for map
        print "LOCATIONS"
    print locations
    return render_template('ItemRecommend.html')

@app.route('/UserRecommend',methods=['GET'])
def user_based():
    print "Most similar reviewers/Users "
    similar_user=functions.mostSimilar(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")
    print dict(similar_user).keys() # to shivani
    print " "

    print "Place Recommendations for a user"
    recommendplc_ub=functions.getRecommendations(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")   #how much will one user like a particular  place
    print recommendplc_ub.keys() # to shivani
    return render_template('UserRecommend.html')

@app.route('/Graph')
def graph():
    return render_template('Graph.html')

# recommendation api's starts here



"""print " "

print "Most similar reviewers/Users "
print functions.mostSimilar(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")

print " "

print "Place Recommendations for a user"
print functions.getRecommendations(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")   #how much will one user like a particular  place

print " "

productData = functions.flipPersonToPlaces(reviewdata.reviews)

print "Finding similar Places "
print functions.mostSimilar(productData,"4iTRjN_uAdAb7_YZDVHJdg")   #Find similar places

print "Computing Item Similarity"
itemSimilarity = functions.computeItemSimilarities(productData)
print itemSimilarity
print " "

print "Item Based Filtering for Recommendations"
print functions.itemBasedFiltering(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw",itemSimilarity)"""

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9000)