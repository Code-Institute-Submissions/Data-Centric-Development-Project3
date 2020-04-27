from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)


def get_database_from_form():
    useremail = request.form.get("useremail")
    results = client.project3.user.find_one({
            "email": (useremail)
        }, {
            'name': 1, 'experience': 1
        })

    return results, useremail


app = Flask(__name__)

# search by email
@app.route('/')
def search_index():

    return render_template('search.template.html')

# when user enters email
@app.route('/', methods=["POST"])
def search_process():
    database, useremail = get_database_from_form()
    # existing user
    if database:
        return render_template('profile.template.html', database=database)
    # new user
    else:
        return render_template('create.template.html', useremail=useremail)

# new user to create account
@app.route('/create',  methods=['POST'])
def createuser():
    client.project3.user.insert_one({
        "name": {
            "firstname": request.form.get("first_name"),
            "lastname": request.form.get("last_name")
        },
        "experience": request.form.get("experience"),
        "certification": request.form.get("certification"),
        "email": request.form.get("useremail")
    })

    database, useremail = get_database_from_form()

    return render_template('profile.template.html', database=database)


# see all dives
@app.route('/dive/<userid>', methods=["GET"])
def search_dive(userid):
    
    dives = client.project3.dive.find({
        "userid": ObjectId(userid)
    }, {
        'location': 1, 'divesite': 1, 'comments':1
    })

    
    
    return render_template('alldivelogs.template.html', dives=dives)



# see all sights
@app.route('/sights/<userid>', methods=["GET"])
def search_sights(userid):
    
    sights = client.project3.sightings.find({
        "userid": ObjectId(userid)
    }, {
        'species': 1, 'photos':1, 'comments':1
    })
    return render_template('allsights.template.html', sights=sights)


# see individual sights
@app.route('/sights_per_dive/<diveid>', methods=["GET"])
def search_sights_per_dive(diveid):
    
    sights = client.project3.sightings.find({
        "diveid": ObjectId(diveid)
    }, {
        'species': 1, 'photos':1, 'comments':1
    })
    return render_template('per_sights.template.html', sights=sights)



# create new dive
@app.route('/createdive/<userid>')
def createdive(userid):

    return render_template('createdive.template.html')

@app.route('/createdive/<userid>', methods=["POST"])
def createdive_process(userid):
    client.project3.dive.insert_one({
        "userid": ObjectId(userid),
        "location": request.form.get("location"),
        "divesite": request.form.get("divesite"),
        "temperature": request.form.get("temperature"),
        "depth": request.form.get("depth"),
        "date": request.form.get("date"),
        "comments": request.form.get("comments")
    })

    dives = client.project3.dive.find({
        "userid": ObjectId(userid)
    }, {
        'location': 1, 'divesite': 1, 'comments':1
    })
    return render_template('alldivelogs.template.html', dives=dives)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
