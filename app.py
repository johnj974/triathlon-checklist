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
    return render_template("home.html", check=mongo.db.checklist.find(),                            # check is assigned variable/ checklist is mongodb doc heading
                                         events=mongo.db.events.find())   
                                                                    

@app.route("/add_list")                                                                             # page for checklist addition
def add_list():
    return render_template("list.html", disciplines=mongo.db.disciplines.find())


@app.route("/blog_list")                                                                            # page for blog
def blog_list():
    return render_template("blog.html", entries=mongo.db.blog.find())


@app.route("/insert_blog", methods=["POST"])                                                        # function to generate new blog
def insert_blog():
    blog = mongo.db.blog 
    blog.insert_one(request.form.to_dict())
    return redirect(url_for("blog_list"))



@app.route("/insert_list", methods=["POST"])                                                        # function to generate new list to home page/maybe change url to index
def insert_list():
    checklist = mongo.db.checklist
    checklist.insert_one(request.form.to_dict())
    return redirect(url_for("index"))


@app.route("/edit_checklist/<checklist_id>")                                                        # function to edit checklist
def edit_checklist(checklist_id):
    the_checklist =  mongo.db.checklist.find_one({"_id": ObjectId(checklist_id)})
    all_disciplines =  mongo.db.disciplines.find()
    return render_template("editlist.html", checklist=the_checklist,
                           disciplines=all_disciplines)



@app.route('/update_list/<checklist_id>', methods=["POST"])
def update_list(checklist_id):
    checklist = mongo.db.checklist
    checklist.update({'_id': ObjectId(checklist_id)},
    {
        'discipline_name': request.form.get('discipline_name'),
        'item1': request.form.get('item1'),
        'item2': request.form.get('item2'),
        'item3': request.form.get('item3'),
        'item4': request.form.get('item4'),
        'item5': request.form.get('item5'),
        'item6': request.form.get('item6'),
        'item7': request.form.get('item7')
    })
    return redirect(url_for('index'))


@app.route("/delete_checklist/<checklist_id>")
def delete_checklist(checklist_id):
    mongo.db.checklist.remove({"_id": ObjectId(checklist_id)})
    return redirect(url_for("index"))


@app.route("/blog", methods=["POST"])                                                # blog function
def blog():
    events = mongo.db.events
    events.insert_one(request.form.to_dict())
    return redirect(url_for("blog_list"))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)