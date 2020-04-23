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
        "name": request.form.get("user_name"),
        "experience": request.form.get("experience")
    })
    return "user details added"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            
######### OR ############


from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host='localhost',
            port=8080,
            debug=True)
            
            
            
    