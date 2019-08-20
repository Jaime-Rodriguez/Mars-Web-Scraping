from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

# Connect to a database. Will create one if not already available.
# db = client.mars_db
# # Drops collection if available to remove duplicates; or creates a new one
# db.mission_to_mars.drop()
# Import the dictionary in the database

@app.route('/scrape/')
def scrape():
   #Call the scrape function from the scrape_mars.py file
   result = scrape_mars.scrape()
   #Store/Write the result disctionary into MongoDB
   # db.mission_to_mars.update(result)
   mongo.db.mission_to_mars.update({}, result, upsert=True)
   return redirect('/')

# Set route

@app.route('/')
def index():
   # Store the entire mars collection in a list
   mars_list = mongo.db.mission_to_mars.find_one()
   print(mars_list)
   # Return the template with the mars_list passed in
   return render_template('index.html', mars_list=mars_list)
if __name__ == "__main__":
   app.run(debug=True)