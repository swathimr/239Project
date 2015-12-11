import random

from flask import Flask,render_template,request,redirect,session
import functions,reviewdata
import reviewdata1
import mysql.connector
#from pyzipcode import ZipCodeDatabase
#zcdb = ZipCodeDatabase()
app = Flask(__name__)
app.secret_key = 'TeStKeY'
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


@app.route('/itravel/')
def hello(name=None):
    return render_template('WelcomePage.html')

@app.route('/dashboard', methods=['POST'])
def hello1():
    _zip = request.form['zip']
    print _zip
    zip_data =[]
    for z in zcdb.get_zipcodes_around_radius(_zip, 10):
        print "Z IS"
        print z.zip
        sql = "SELECT B_NAME, PHOTO_URL, RATING, ADDRESS from BUSINESS_CA WHERE ADDRESS LIKE '%' ORDER BY RATING DESC LIMIT 10"
        cursor.execute(sql)
        data = cursor.fetchall()
        print "$$$$$$$$$ DATA $$$$$$$$$"
        print data
        print cursor._executed.decode("utf-8")
        if data != None:
            zip_data.append([data[0],data[1],data[2], data[3], data[4],data[5],data[6],data[7],data[8],data[9]])
    print "@@@@@@ ZIP DATA @@@@@@@@"
    print zip_data
    return render_template('Dashboard.html', zipData = zip_data)


@app.route('/login',methods=['POST'])
def login():
    session.clear
    _email = request.form['email']
    sql = ("SELECT USER_ID from USER where USER_EMAIL = '%s'" % _email)
    cursor.execute(sql)
    data = cursor.fetchone()
    if data!=None:
        session['user_id']=data
        print "Welcome user::"+session['user_id'][0]
        return render_template('UserHomePage.html',user_id=data)
    else:
        return redirect('itravel')

@app.route('/ItemRecommend')
def Item_based():
    user_id=session['user_id'][0]
    productData = functions.flipPersonToPlaces(reviewdata1.reviews)
    print "Finding similar Places " # for single place
    similar_item=functions.mostSimilar(productData,"4iTRjN_uAdAb7_YZDVHJdg")
    print dict(similar_item)
    b_data=[]
    for bid in dict(similar_item).keys():
        sql = ("SELECT B_NAME, PHOTO_URL,RATING from BUSINESS_CA where B_ID = '%s'" % bid)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            b_data.append([data[0],data[1],data[2]])
    print b_data
    print "******************"
    print "Computing Item Similarity" # for entire product data
    itemSimilarity = functions.computeItemSimilarities(productData)
    print itemSimilarity
    print "******************"
    print "Item Based Filtering for Recommendations"
    recommendedplc_ib=functions.itemBasedFiltering(reviewdata1.reviews,str(user_id),itemSimilarity)
    print recommendedplc_ib.keys() #send to shivani

    locations =[]
    for bid in recommendedplc_ib.keys():
        sql = ("SELECT B_NAME, LATITUDE, LONGITUDE, ADDRESS, RATING from BUSINESS_CA where B_ID = '%s'" % bid)
        cursor.execute(sql)
        data_map = cursor.fetchone()
        if data_map!=None:
            value=[str(data_map[0]),float(data_map[1]),float(data_map[2]),str(data_map[3]),data_map[4]]
            locations.append(value)
    print "locations is"
    print locations
    return render_template('ItemRecommend.html',location=locations,similarplaces=b_data)

@app.route('/UserRecommend',methods=['GET'])
def user_based():
    user_id=session['user_id'][0]
    print "Most similar reviewers/Users "
    similar_user=functions.mostSimilar(reviewdata1.reviews,str(user_id))
    #similar_user=functions.mostSimilar(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")
    u_data = []
    print dict(similar_user).keys()
    print "###########"
    for uid in dict(similar_user).keys():
        sql = ("SELECT USER_NAME from USER where USER_ID = '%s'" % uid)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            rating= random.randint(3,5)
            u_data.append([data[0],rating])
    print "U_DATA"
    print u_data
    print "###########"

    print "Place Recommendations for a user"
    recommendplc_ub=functions.getRecommendations(reviewdata1.reviews,str(user_id))   #how much will one user like a particular  place

    print "************"
    locations =[]
    for bid in recommendplc_ub.keys():
        sql = ("SELECT B_NAME, LATITUDE, LONGITUDE, ADDRESS, RATING from BUSINESS_CA where B_ID = '%s'" % bid)
        cursor.execute(sql)
        data_map = cursor.fetchone()
        if data_map!=None:
            value=[str(data_map[0]),float(data_map[1]),float(data_map[2]),str(data_map[3]),data_map[4]]
            locations.append(value)
    return render_template('UserRecommend.html', location=locations,similarusers=u_data)

@app.route('/Graph')
def graph():
    return render_template('Graph.html')

@app.route('/AvgRating')
def rating_graph():
    return render_template('AvgRating.html')

@app.route('/dashboard')
def dashboard():
    return render_template('UserHomePage.html')

# dummy functionality
@app.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    _name = request.form['name']
    _email = request.form['email']
    _password = request.form['password']
    #add user information into db
    print _email+"::"+_name+"::"+_password
    return render_template('UserHomePage.html',email=_email)

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9000)