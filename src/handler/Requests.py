from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify,request
from bson.json_util import dumps

app = Flask(__name__)
mongo1 = PyMongo(app, uri = 'mongodb://localhost:27017/Actions')
mongo2 = PyMongo(app, uri = 'mongodb://localhost:27017/sampleInput')

@app.route('/notes')
def notes():
    notes = mongo1.db.Events.find()
    resp = dumps(notes)
    return resp

@app.route('/getNotesByUserID/<id>')
def getNotesByUserID(id):
    patientResp = mongo1.db.Events.find_one({"patientID":id})
    resp = dumps(patientResp)
    return resp

@app.route('/setNotesByUserID/',methods=['POST'])
def setNotesByUserID():
    _json = request.json
    patientID = _json['PatientID']
    text = _json['Text']
    actual = _json['Actual']

    mongo2.db.Details.insert({"PatientID":patientID,"Text":text,"Actual":actual})
    resp = jsonify("Added Successfully")
    resp.status_code = 200
    return resp

def main():
    app.run()

