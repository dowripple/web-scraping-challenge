from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

# create instance of flask
app = Flask(__name__)

# establish pymongo connection
app.config['Mongo_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# the index page
@app.route("/")
def index():
    
    # get the 1 row of mars data from the db, should be freshly scraped
    mars_stuff = mongo.db.mars_data.find_one()

    return render_template("index.html", martian_data = mars_stuff)

@app.route("/scrape")
def scrape():

    # run the program to scrape mars data
    latest_mars_data = scrape_mars.scrape()

    # insert one row into database
    mongo.db.mars_data.update({}, latest_mars_data, upsert = True)

    # redirect to home page
    return redirect('/')    

if __name__ == "__main__":
    app.run(debug=True)