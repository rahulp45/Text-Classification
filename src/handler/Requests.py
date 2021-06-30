from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Actions"
mongo = PyMongo(app)

@app.route('/notes')
def notes():
    notes = mongo.db.Events.find()
    resp = dumps(notes)
    return resp

@app.route('/getNotesByUserID/<id>')
def getNotesByUserID(id):
    patientResp = mongo.db.Events.find_one({"patientID":id})
    resp = dumps(patientResp)
    return resp

def main():
    app.run()

