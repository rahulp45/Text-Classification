from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/Actions"
client = MongoClient(connection_string)
db = client.get_database("Actions")
collection = db.get_collection("Events")

def insert_into_database(ResultObj):
    for feature in ResultObj:
        if(db.Events.find({"patientID":feature[0]}).count()>0):
            db.Events.update({"patientID":feature[0]},
                             {"$push":{"Response":
                                 {
                                    "Event":feature[1],
                                    "When":feature[2],
                                    "Date":feature[3],
                                    "Location":feature[4],
                                     "Text":feature[5]
                                 }
                             }})
        else:
            document={"patientID":feature[0],
                       "Response":[
                                {
                                    "Event":feature[1],
                                    "When":feature[2],
                                    "Date":feature[3],
                                    "Location":feature[4],
                                     "Text":feature[5]
                                }]}
            collection.insert_one(document)