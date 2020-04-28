from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from bson.objectid import ObjectId
import all_functions as af
from dotenv import load_dotenv
load_dotenv()


MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)





app = Flask(__name__)

# search by email
@app.route('/')
def search_index():

    return render_template('search.template.html')

# when user enters email
@app.route('/', methods=["POST"])
def search_process():
    
    database, useremail = af.get_database_from_form()
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
    database, useremail = af.get_database_from_form()

    return render_template('profile.template.html', database=database)


# see all dives
@app.route('/dive/<userid>')
def search_dive(userid):
    dives = af.all_dives(userid)
    return render_template('alldivelogs.template.html', dives=dives)

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
        'location': 1, 'divesite': 1, 'depth': 1, 'temperature': 1, 'date': 1, 'comments': 1, 'userid': 1
    })
    return render_template('alldivelogs.template.html', dives=dives)



# Edit dive
@app.route('/editdive/<diveid>/<userid>')
def edit_dive(diveid,userid):

    dives = client.project3.dive.find_one({
        "_id": ObjectId(diveid)
    }, {
        'location': 1, 'divesite': 1, 'comments':1, 'userid':1, 'temperature':1, 'depth':1, 'date':1
    })
    return render_template('editdive.template.html', dives=dives)


@app.route('/editdive/<diveid>/<userid>', methods=["POST"])
def edit_dive_process(diveid,userid):
    client.project3.dive.update_one({
        "_id":ObjectId(diveid)
    },{
        "$set":{
        "location": request.form.get("location"),
        "divesite": request.form.get("divesite"),
        "temperature": request.form.get("temperature"),
        "depth": request.form.get("depth"),
        "date": request.form.get("date"),
        "comments": request.form.get("comments")
    }
    })

    dives = client.project3.dive.find({
        "userid": ObjectId(userid)
    }, {
        'location': 1, 'divesite': 1, 'depth': 1, 'temperature': 1, 'date': 1, 'comments': 1, 'userid': 1
    })
    return render_template('alldivelogs.template.html', dives=dives)


# create new sighting
@app.route('/createsighting/<diveid>/<userid>')
def create_sighting(diveid,userid):
    return render_template('createsighting.template.html')

@app.route('/createsighting/<diveid>/<userid>', methods=["POST"])
def create_sighting_process(diveid,userid):
    
    client.project3.sightings.insert_one({
        "userid": ObjectId(userid),
        "diveid": ObjectId(diveid),
        "species": request.form.get("species"),
        "photos": request.form.get("photos"),
        "comments": request.form.get("comments")
    })

    sights = af.get_sights_userid(userid)

    return render_template('allsights.template.html', sights=sights)

# see all sights
@app.route('/sights/<userid>')
def search_sights(userid):
    sights = af.get_sights_userid(userid)
    return render_template('allsights.template.html', sights=sights)


# see individual sights
@app.route('/sights_per_dive/<diveid>')
def search_sights_per_dive(diveid):
    sights = af.get_sights_diveid(diveid)
    return render_template('per_sights.template.html', sights=sights)



# Edit Sighting
@app.route('/editsight/<sightid>/<userid>')
def edit_sight(sightid,userid):

    sights = client.project3.sightings.find_one({
        "_id": ObjectId(sightid)
    }, {
        'species': 1, 'photos':1, 'comments':1, 'userid':1, 'diveid':1
    })
    return render_template('editsight.template.html', sights=sights)


@app.route('/editsight/<sightid>/<userid>', methods=["POST"])
def edit_sight_process(sightid,userid):
    client.project3.sightings.update_one({
        "diveid": ObjectId(diveid)
    },{
        "$set":{
        "species": request.form.get("species"),
        "photos": request.form.get("photos"),
        "comments": request.form.get("comments")
    }
    })

    sights = af.get_sights_userid(userid)
    
    return render_template('allsights.template.html', sights=sights)




# Delete sightings
@app.route('/delete/<userid>/<diveid>/<sightid>/<delete_status>')
def delete(userid, diveid, sightid, delete_status):
   
    return render_template('delete.template.html')

@app.route('/delete/<userid>/<diveid>/<sightid>/<delete_status>' , methods=["POST"])
def delete_process(userid, diveid, sightid, delete_status):
    delete_status = delete_status
    if delete_status == 's':
        client.project3.sightings.delete_one({
            "_id": ObjectId(sightid),
        })

        sights = af.get_sights_userid(userid)
        return render_template('allsights.template.html', sights=sights)

    elif delete_status == 'd':
        client.project3.dive.delete_one({
            "_id": ObjectId(diveid),
        })

        client.project3.sightings.delete_many({
            "diveid": ObjectId(diveid),
        })

        dives = af.all_dives(userid)
        return render_template('alldivelogs.template.html', dives=dives)

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

        return redirect(url_for('search_index'))
# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)