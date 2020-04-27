from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo

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