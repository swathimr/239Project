from flask import Flask,render_template,request,session
import functions,reviewdata

app = Flask(__name__)

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

@app.route('/itemRecommend',methods=['GET'])
def item_based():
    return render_template('UserHomePage.html')

@app.route('/userRecommend',methods=['GET'])
def user_based():
    return render_template('UserHomePage.html')

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

print " "
print "This wont work we need to remove the below one alone"
print "Finding user Recommendations for a product"
print functions.getRecommendations(productData,"ZRm8fSEBn8DsSLD4o7T4hQ") #Out of the people Who havent seen the place Who will like this place ?
print " "


print "Computing Item Similarity"
itemSimilarity = functions.computeItemSimilarities(productData)
print itemSimilarity
print " "

print "Item Based Filtering for Recommendations"
print functions.itemBasedFiltering(reviewdata.reviews,"T9hGHsbJW9Hw1cJAlIAWmw",itemSimilarity)


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9000)