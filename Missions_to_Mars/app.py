from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    print("I am on index.html")
    mars_data = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars_data)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)