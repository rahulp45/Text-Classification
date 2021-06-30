from pymongo import MongoClient
from helper.Features import Features

connection_string = "mongodb://localhost:27017/sampleInput"
client = MongoClient(connection_string)
db = client.get_database("sampleInput")
collection = db.get_collection("Details")

#import data from mongodb
def parseInput():
    featureObjects = []
    for document in db.Details.find():
        patientID = document.get("PatientID")
        text = document.get("Text")
        actual = document.get("Actual")
        feature = Features(patientID, text, actual)
        featureObjects.append(feature)
    return featureObjects
