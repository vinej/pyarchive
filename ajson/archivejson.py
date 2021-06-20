import json

class ArchiveJson:
    def load(self, file):
        fObj = open(file)
        return json.load(fObj)
    #def
#def
