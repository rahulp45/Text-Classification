from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Actions"
mongo = PyMongo(app)

@app.route('/allPatients')
def allPatients():
    allPatients = mongo.db.Events.find()
    All = dumps(allPatients)
    return All

@app.route('/patientResponse/<id>')
def response(id):
    patientResp = mongo.db.Events.find_one({"patientID":id})
    resp = dumps(patientResp)
    return resp

def main():
    app.run()

