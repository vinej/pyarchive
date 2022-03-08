import json

'''
Read a pyarchive json file in memory
'''
class ArchiveJson:
    def load(self, file):
        fObj = open(file)
        return json.load(fObj)
    #def
#def
