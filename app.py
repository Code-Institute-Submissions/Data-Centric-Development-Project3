from flask import Flask, render_template, request, redirect, url_for
import os
import math
import pymongo
from bson.objectid import ObjectId
import all_functions as af
from dotenv import load_dotenv
load_dotenv()


MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
uploadcare_public_key = os.environ.get('UPLOADCARE_PUBLIC_KEY')





app = Flask(__name__)

# search by email
@app.route('/')
def index():
    # to find the latest 5 entries in sightings collection - create a default photo
    lastentry = client.project3.sightings.find().sort("_id", -1).limit(5)

    return render_template('index.template.html', lastentry=lastentry)

# when user enters email
@app.route('/', methods=["POST"])
def search_process():

    database, useremail = af.get_database_from_form()
    # existing user
    if database:
        return render_template('profile.template.html', database=database)
    # new user
    else:
        return render_template('createuser.template.html', useremail=useremail, uploadcare_public_key=uploadcare_public_key)

# go back to profile
@app.route('/profile/<userid>')
def profile(userid):
    database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })

    return render_template('profile.template.html', database=database)


# new user to create account
@app.route('/create',  methods=['POST'])
def createuser():
    # if no user profile photo uploaded
    if request.form.get("photos") == '':
        client.project3.user.insert_one({
            "name": {
                "firstname": (request.form.get("first_name")).title(),
                "lastname": (request.form.get("last_name")).title()
            },
            "experience": (request.form.get("experience")).title(),
            "certification": (request.form.get("certification")).upper(),
            "email": (request.form.get("useremail")).title(),
            "photos": 'https://ucarecdn.com/4c0ef6a3-a23e-45bc-9066-2ab52d39baae/'
        })

    else:
        client.project3.user.insert_one({
            "name": {
                "firstname": (request.form.get("first_name")).title(),
                "lastname": (request.form.get("last_name")).title()
            },
            "experience": (request.form.get("experience")).title(),
            "certification": (request.form.get("certification")).title(),
            "email": (request.form.get("useremail")).title(),
            "photos": request.form.get("photos")
            })

    database, useremail = af.get_database_from_form()

    return render_template('profile.template.html', database=database, uploadcare_public_key=uploadcare_public_key)


# see all dives
@app.route('/dive/<userid>')
def search_dive(userid):
    # pagination
    entry_per_page = 5
    max_pages = math.ceil(af.all_dives(userid).count() / entry_per_page)
    current_page = int(request.args.get('page', 1))
    listings = af.all_dives(userid).skip((current_page-1)*entry_per_page).limit(entry_per_page)

    return render_template('alldivelogs.template.html', results=listings, max_pages=max_pages, current_page=current_page)

# create new dive
@app.route('/createdive/<userid>')
def createdive(userid):
    return render_template('createdive.template.html')


@app.route('/createdive/<userid>', methods=["POST"])
def createdive_process(userid):
    client.project3.dive.insert_one({
        "userid": ObjectId(userid),
        "location": (request.form.get("location")).title(),
        "divesite": (request.form.get("divesite")).title(),
        "temperature": (request.form.get("temperature")).title(),
        "depth": (request.form.get("depth")).title(),
        "date": request.form.get("date"),
        "comments": (request.form.get("comments")).title()
    })

    database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
    return render_template('profile.template.html', database=database)


# Edit dive
@app.route('/editdive/<diveid>/<userid>')
def edit_dive(diveid, userid):

    dives = af.dive_diveid(diveid)
    return render_template('editdive.template.html', dives=dives)


@app.route('/editdive/<diveid>/<userid>', methods=["POST"])
def edit_dive_process(diveid, userid):
    client.project3.dive.update_one({
        "_id": ObjectId(diveid)
        }, {
        "$set": {
            "location": (request.form.get("location")).title(),
            "divesite": (request.form.get("divesite")).title(),
            "temperature": (request.form.get("temperature")).title(),
            "depth": (request.form.get("depth")).title(),
            "date": request.form.get("date"),
            "comments": (request.form.get("comments")).title()
        }
    })

    database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
    return render_template('profile.template.html', database=database)


# create new sighting
@app.route('/createsighting/<diveid>/<userid>')
def create_sighting(diveid, userid):
    return render_template('createsighting.template.html', uploadcare_public_key=uploadcare_public_key)


@app.route('/createsighting/<diveid>/<userid>', methods=["POST"])
def create_sighting_process(diveid, userid):
    # if no sighting photos upload by user - create a default image
    if request.form.get("photos") == '':
        client.project3.sightings.insert_one({
            "userid": ObjectId(userid),
            "diveid": ObjectId(diveid),
            "species": (request.form.get("species")).title(),
            "photos": 'https://ucarecdn.com/91ca9fa4-d421-4d73-a70f-350e75e0ab8b/',
            "comments": (request.form.get("comments")).title()
        })

    else:
        client.project3.sightings.insert_one({
            "userid": ObjectId(userid),
            "diveid": ObjectId(diveid),
            "species": (request.form.get("species")).title(),
            "photos": request.form.get("photos"),
            "comments": (request.form.get("comments")).title()
        })

    database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
    return render_template('profile.template.html', database=database)

# see all sights
@app.route('/sights/<userid>')
def search_sights(userid):

    # pagination
    entry_per_page = 5
    max_pages = math.ceil(af.get_sights_userid(userid).count() / entry_per_page)
    current_page = int(request.args.get('page', 1))
    listings = af.get_sights_userid(userid).skip((current_page-1)*entry_per_page).limit(entry_per_page)

    return render_template('allsights.template.html', results=listings, max_pages=max_pages, current_page=current_page)


# see individual sights
@app.route('/sights_per_dive/<diveid>')
def search_sights_per_dive(diveid):

     # pagination
    entry_per_page = 5
    max_pages = math.ceil(af.get_sights_diveid(diveid).count() / entry_per_page)
    current_page = int(request.args.get('page', 1))
    listings = af.get_sights_diveid(diveid).skip((current_page-1)*entry_per_page).limit(entry_per_page)

    return render_template('per_sights.template.html', results=listings, max_pages=max_pages, current_page=current_page)


# Edit Sighting
@app.route('/editsight/<sightid>/<userid>')
def edit_sight(sightid, userid):

    sights = client.project3.sightings.find_one({
        "_id": ObjectId(sightid)
    }, {
        'species': 1, 'photos': 1, 'comments': 1, 'userid': 1, 'diveid': 1
    })
    return render_template('editsight.template.html', sights=sights, uploadcare_public_key=uploadcare_public_key)


@app.route('/editsight/<sightid>/<userid>', methods=["POST"])
def edit_sight_process(sightid, userid):
    client.project3.sightings.update_one({
        "_id": ObjectId(sightid)
    }, {
        "$set": {
            "species": (request.form.get("species")).title(),
            "photos": request.form.get("photos"),
            "comments": (request.form.get("comments")).title()
    }
    })

    database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
    return render_template('profile.template.html', database=database)


# Delete sightings
@app.route('/delete/<userid>/<diveid>/<sightid>/<delete_status>')
def delete(userid, diveid, sightid, delete_status):
    return render_template('delete.template.html')


@app.route('/delete/<userid>/<diveid>/<sightid>/<delete_status>', methods=["POST"])
def delete_process(userid, diveid, sightid, delete_status):
    delete_status = delete_status
    # delete sightings
    if delete_status == 's':
        client.project3.sightings.delete_one({
            "_id": ObjectId(sightid),
        })

        database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
        return render_template('profile.template.html', database=database)
    # delete dive log
    elif delete_status == 'd':
        client.project3.dive.delete_one({
            "_id": ObjectId(diveid),
        })

        client.project3.sightings.delete_many({
            "diveid": ObjectId(diveid),
        })

        database = client.project3.user.find_one({
            "_id": ObjectId(userid)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })
        return render_template('profile.template.html', database=database)
    # delete user
    elif delete_status == 'u':
        client.project3.user.delete_one({
            "_id": ObjectId(userid),
        })

        client.project3.dive.delete_many({
            "userid": ObjectId(userid),
        })

        client.project3.sightings.delete_many({
            "userid": ObjectId(userid),
        })

        return redirect(url_for('index'))


@app.route('/searchall/', methods=["POST"])
def search_all_process():
    search_country = client.project3.dive.find_one({
        "location": (request.form.get("search")).title()
    })

    search_divesite = client.project3.dive.find_one({
        "divesite": (request.form.get("search")).title()
    })

    search_specie = client.project3.sightings.find_one({
        "species": (request.form.get("search")).title()
    })

    if search_country:
        status = 'location'
        search_result = client.project3.dive.find({
            "location": (request.form.get("search")).title()
        }, {
            'location': 1, 'divesite': 1, 'depth': 1, 'temperature': 1, 'date': 1, 'comments': 1, 'userid': 1
        })
        return render_template('search_all.template.html', search_result=search_result, status=status)

    elif search_divesite:
        status = 'location'
        search_result = client.project3.dive.find({
            "divesite": (request.form.get("search")).title()
        }, {
            'location': 1, 'divesite': 1, 'depth': 1, 'temperature': 1, 'date': 1, 'comments': 1, 'userid': 1
        })
        return render_template('search_all.template.html', search_result=search_result, status=status)

    elif search_specie:
        status = 'species'
        search_result = client.project3.sightings.find({
            "species": (request.form.get("search")).title()
        }, {
            'species': 1, 'photos': 1, 'comments': 1, 'userid': 1, 'diveid': 1
        })
        return render_template('search_all.template.html', search_result=search_result, status=status)

    else:
        status = 'nothing'
        return render_template('search_all.template.html', status=status)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)