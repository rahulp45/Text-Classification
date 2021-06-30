
class Event(object):

    def __init__(self,patientID, type, rel_date, abs_date, location):
        self.patientID=patientID
        self.type = type
        self.rel_date = rel_date
        self.abs_date = abs_date
        self.location = location

    
    