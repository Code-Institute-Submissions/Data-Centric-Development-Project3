from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)


app = Flask(__name__)

# search by email
@app.route('/')
def search_index():

    return render_template('search.template.html')


@app.route('/', methods=["POST"])
def search_process():
    useremail = request.form.get("useremail")
    database = client.project3.user.find_one({
        "email": (useremail)
    }, {
        'name': 1, 'experience': 1
    })
    # existing user
    if database:
        return render_template('show.template.html', database=database)
    # new user
    else:
        return render_template('create.template.html', useremail=useremail)


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

    useremail = request.form.get("useremail")
    database = client.project3.user.find_one({
            "email": (useremail)
        }, {
            'name': 1, 'experience': 1
        })

    return render_template('show.template.html', database=database)


# see dives
@app.route('/dive/<userid>', methods=["GET"])
def search_dive(userid):
    
    dives = client.project3.dive.find_one({
        "userid": ObjectId(userid)
    }, {
        'location': 1, 'divesite': 1, 'comments':1
    })
    return render_template('divelogs.template.html', dives=dives)



# see sights
@app.route('/sights/<userid>', methods=["GET"])
def search_sights(userid):
    
    sights = client.project3.sightings.find_one({
        "userid": ObjectId(userid)
    }, {
        'species': 1, 'photos':1, 'comments':1
    })
    return render_template('sights.template.html', sights=sights)




# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
