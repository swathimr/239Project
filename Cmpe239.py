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
#db = mysql.connector.connect(**config)


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
    print functions.mostSimilar(productData,"4iTRjN_uAdAb7_YZDVHJdg")

    print "Computing Item Similarity"
    itemSimilarity = functions.computeItemSimilarities(productData)
    print itemSimilarity
    print " "

    #get shop name,lat,long,rating for these shops write api
    print "Item Based Filtering for Recommendations"
    print functions.itemBasedFiltering(reviewdata.reviews,user_id,itemSimilarity)
    return render_template('ItemRecommend.html')

@app.route('/UserRecommend',methods=['GET'])
def user_based():
    return render_template('UserRecommend.html')

@app.route('/Graph')
def graph():
    return render_template('Graph.html')

# recommendation api's starts here

print "Most similar reviewers/Users "
print functions.mostSimilar(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")

print " "

print "Place Recommendations for a user"
print functions.getRecommendations(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw")   #how much will one user like a particular  place

print " "

productData = functions.flipPersonToPlaces(reviewdata.reviews)

print "Finding similar Places "
print functions.mostSimilar(productData,"4iTRjN_uAdAb7_YZDVHJdg")   #Find similar places

"""print " "
print "This wont work we need to remove the below one alone"
print "Finding user Recommendations for a product"
print functions.getRecommendations(productData,"ZRm8fSEBn8DsSLD4o7T4hQ") #Out of the people Who havent seen the place Who will like this place ?
print " "
print "Computing Item Similarity"
itemSimilarity = functions.computeItemSimilarities(productData)
print itemSimilarity
print " "

print "Item Based Filtering for Recommendations"
print functions.itemBasedFiltering(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw",itemSimilarity)"""

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9000)