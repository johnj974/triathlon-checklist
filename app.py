import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_table import Table

from os import path
if path.exists("env.py"):
    import env

MONGO_URI = os.environ.get("TRIDATA")

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "triathlon_checklist"
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)


# home page
@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html", check=mongo.db.checklist.find(),
                           types=mongo.db.types.find())


# function to generate new checklist to home page
@app.route("/insert_list", methods=["POST"])
def insert_list():
    checklist = mongo.db.checklist
    checklist.insert_one(request.form.to_dict())
    return redirect(url_for("index"))


# page for checklist addition
@app.route("/add_list")
def add_list():
    return render_template("list.html",
                           disciplines=mongo.db.disciplines.find(),
                           events=mongo.db.events.find(),
                           types=mongo.db.types.find())


# function to edit checklist
@app.route("/edit_checklist/<checklist_id>")
def edit_checklist(checklist_id):
    the_checklist = mongo.db.checklist.find_one({"_id": ObjectId(checklist_id)})
    all_disciplines = mongo.db.disciplines.find()
    return render_template("editlist.html", checklist=the_checklist,
                           disciplines=all_disciplines)


# path to update checklist/populate updated checklist
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


# function to delete checklist
@app.route("/delete_checklist/<checklist_id>")
def delete_checklist(checklist_id):
    mongo.db.checklist.remove({"_id": ObjectId(checklist_id)})
    return redirect(url_for("index"))


# page for blog
@app.route("/blog_list")
def blog_list():
    return render_template("blog.html", entries=mongo.db.blog.find())


# function to generate new blog
@app.route("/insert_blog", methods=["POST"])
def insert_blog():
    blog = mongo.db.blog
    blog.insert_one(request.form.to_dict())
    return redirect(url_for("blog_list"))


# function to delete blog
@app.route("/delete_blog/<blog_id>")
def delete_blog(blog_id):
    mongo.db.blog.remove({"_id": ObjectId(blog_id)})
    return redirect(url_for("blog_list"))


# function to edit blog
@app.route("/edit_blog/<blog_id>")
def edit_blog(blog_id):
    the_blog = mongo.db.blog.find_one({"_id": ObjectId(blog_id)})
    return render_template("editblog.html", blog=the_blog)


# path to update blog/populate updated blog
@app.route('/update_blog/<blog_id>', methods=["POST"])
def update_blog(blog_id):
    blog = mongo.db.blog
    blog.update({'_id': ObjectId(blog_id)},
                {
        'blog_title': request.form.get('blog_title'),
        'blog_content': request.form.get('blog_content')
    })
    return redirect(url_for('blog_list'))


# page for events list
@app.route("/event_list")
def event_list():
    return render_template("events.html", events=mongo.db.events.find())


# function to generate new event list to event page
@app.route("/insert_event", methods=["POST"])
def insert_event():
    events = mongo.db.events
    events.insert_one(request.form.to_dict())
    return redirect(url_for("event_list"))


# function to delete event list
@app.route("/delete_events/<events_id>")
def delete_events(events_id):
    mongo.db.events.remove({"_id": ObjectId(events_id)})
    return redirect(url_for("event_list"))


# function to edit event list
@app.route("/edit_eventlist/<events_id>")
def edit_eventlist(events_id):
    the_eventlist = mongo.db.events.find_one({"_id": ObjectId(events_id)})
    all_types = mongo.db.types.find()
    return render_template("editeventlist.html", events=the_eventlist,
                           types=all_types)


# path to update eventlist/populate updated eventlist
@app.route('/update_eventlist/<events_id>', methods=["POST"])
def update_eventlist(events_id):
    events = mongo.db.events
    events.update({'_id': ObjectId(events_id)},
                  {
                    'discipline_type': request.form.get('discipline_type'),
                    'name': request.form.get('name'),
                    'location': request.form.get('location'),
                    'date': request.form.get('date'),
                    'swim_time': request.form.get('swim_time'),
                    'cycle_time': request.form.get('cycle_time'),
                    'run_time': request.form.get('run_time')
                })
    return redirect(url_for('event_list'))


# record event page
@app.route("/record_event")
def record_event():
    return render_template("recordevent.html",
                           disciplines=mongo.db.disciplines.find(),
                           events=mongo.db.events.find(),
                           types=mongo.db.types.find())


# page for equipment suggestions
@app.route("/equipment_list")
def equipment_list():
    return render_template("equipment.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
