import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
    import env

MONGO_URI = os.environ.get("tridata")                                                               #environmental variable

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "triathlon_checklist"
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html", check=mongo.db.checklist.find())                            # check is assigned variable/ checklist is mongodb doc heading

@app.route("/add_list")
def add_list():
    return render_template("list.html", check=mongo.db.checklist.find())

@app.route("/complete_list")
def complete_list():
    return render_template("index.html", check=mongo.db.checklist.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    checklists = mongo.db.checklist
    checklists.insert_one(request.form.to_dict())
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)