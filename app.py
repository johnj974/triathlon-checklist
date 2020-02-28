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



@app.route("/")                                                                                     # home page
@app.route("/home")
def index():
    return render_template("home.html", check=mongo.db.checklist.find(),                            # check is assigned variable/ checklist is mongodb doc heading
                                        types=mongo.db.types.find())                                # events is assigned variable to mongodb heading


@app.route("/insert_list", methods=["POST"])                                                        # function to generate new checklist to home page
def insert_list():
    checklist = mongo.db.checklist
    checklist.insert_one(request.form.to_dict())
    return redirect(url_for("index"))
                                      
                                        
@app.route("/add_list")                                                                             # page for checklist addition
def add_list():
    return render_template("list.html", disciplines=mongo.db.disciplines.find(),
                                        events=mongo.db.events.find(),
                                        types=mongo.db.types.find())


@app.route("/edit_checklist/<checklist_id>")                                                        # function to edit checklist
def edit_checklist(checklist_id):
    the_checklist =  mongo.db.checklist.find_one({"_id": ObjectId(checklist_id)})
    all_disciplines =  mongo.db.disciplines.find()
    return render_template("editlist.html", checklist=the_checklist,
                           disciplines=all_disciplines)


@app.route('/update_list/<checklist_id>', methods=["POST"])                                         # update path to update checklist/populate editlist 
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


@app.route("/delete_checklist/<checklist_id>")                                                      # function to delete checklist
def delete_checklist(checklist_id):
    mongo.db.checklist.remove({"_id": ObjectId(checklist_id)})
    return redirect(url_for("index"))



@app.route("/blog_list")                                                                            # page for blog
def blog_list():
    return render_template("blog.html", entries=mongo.db.blog.find())


@app.route("/insert_blog", methods=["POST"])                                                        # function to generate new blog
def insert_blog():
    blog = mongo.db.blog 
    blog.insert_one(request.form.to_dict())
    return redirect(url_for("blog_list"))



@app.route("/event_list")                                                                            # page for events list
def event_list():
    return render_template("events.html", events=mongo.db.events.find())


@app.route("/insert_event", methods=["POST"])                                                        # function to generate new event list to event page
def insert_event():
    events = mongo.db.events
    events.insert_one(request.form.to_dict())
    return redirect(url_for("event_list"))


@app.route("/delete_events/<events_id>")                                                             # function to delete event list
def delete_events(events_id):
    mongo.db.events.remove({"_id": ObjectId(events_id)})
    return redirect(url_for("event_list"))

@app.route("/edit_eventlist/<events_id>")                                                            # function to edit event list
def edit_eventlist(events_id):
    the_eventlist =  mongo.db.events.find_one({"_id": ObjectId(events_id)})
    all_types =  mongo.db.types.find()
    return render_template("editeventlist.html", events=the_eventlist,
                           types=all_types)







if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)


