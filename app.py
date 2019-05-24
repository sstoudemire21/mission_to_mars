from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars = mongo.db.collection.find_one()
    try:

        return render_template("index.html", mars_data=mars)
    except: 

        return redirect('/scrape', code=302)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_data = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)

    return render_template('index.html')

if __name__ == "__main__":  
    app.run(debug= True)