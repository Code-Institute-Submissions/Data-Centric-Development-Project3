from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from bson.objectid import ObjectId


MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

def get_database_from_form():
    useremail = (request.form.get("useremail")).title()
    results = client.project3.user.find_one({
            "email": (useremail)
        }, {
            'name': 1, 'experience': 1, 'certification':1, 'photos':1
        })

    return results, useremail


def get_sights_userid(userid):
    sights = client.project3.sightings.find({
        "userid": ObjectId(userid)
    }, {
        'species': 1, 'photos':1, 'comments':1, 'userid':1, 'diveid':1
    })

    return sights


def get_sights_diveid(diveid):
    sights = client.project3.sightings.find({
        "diveid": ObjectId(diveid)
    }, {
        'species': 1, 'photos':1, 'comments':1, 'userid':1, 'diveid':1
    })

    return sights

def all_dives(userid):
    dives = client.project3.dive.find({
        "userid": ObjectId(userid)
    }, {
        'location': 1, 'divesite': 1, 'depth': 1, 'temperature': 1, 'date': 1, 'comments': 1, 'userid': 1
    })
    
    return dives


def dive_diveid(diveid):
    dives = client.project3.dive.find_one({
        "_id": ObjectId(diveid)
    }, {
        'location': 1, 'divesite': 1, 'comments':1, 'userid':1, 'temperature':1, 'depth':1, 'date':1
    })

    return dives