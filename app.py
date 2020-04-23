from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('create.template.html')


@app.route('/',  methods=['POST'])
def create():
    client.project3.user.insert_one({
        "name": {
            "firstname": request.form.get("first_name"),
            "lastname": request.form.get("last_name")
        },
        "experience": request.form.get("experience"),
        "certification": request.form.get("certification")
    })
    return "user details added"




@app.route('/searchuser')
def search_index():

    return render_template('search.template.html')



@app.route('/searchuser/<useremail>', methods=['POST'])
def search_process(useremail):

    database_email= client.project3.user.find_one({
        "email":(useremail)
    },{
        'name':1,'experience':1
    })

    if database_email:
        return render_template('show.template.html',database_email=database_email)

    else:
        return('Not valid')


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
