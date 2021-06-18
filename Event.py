
class Event(object):

    def __init__(self, type, rel_date, abs_date, location):
        self.type = type
        self.rel_date = rel_date
        self.abs_date = abs_date
        self.location = location

#     def format(self):
#         formattedResult = ""
#         if self.location != "":
#             formattedResult = "Event : {}, when: {}, where: {}".format(self.type, self.date, self.location)
#         else:
#             formattedResult = "Event : {}, when: {}".format(self.type, self.date)

#         return formattedResult
    
    
    