from task.array import Array
from task.csv import Csv
from task.query import Query

class Task:
    def __init__(self, data):
        self.mapmem = {}
        self.mapref = {}
        self.maptask = []
        mapjsontask = data['Tasks']
        for t in mapjsontask:
            self.maptask.append(t)
        #for
    #def

    def run(self, mapcon):
        i = 1
        for t in self.maptask:
            ct = self.get_task(t)
            ct.run(self.mapmem, self.mapref, mapcon, i)
            i = i + 1
        #for
    #def

    def get_task(self, onetask):
        if onetask['Kind'] == 'array':
            return Array(onetask)
        elif onetask['Kind'] == 'csv':
            return Csv(onetask)
        elif onetask['Kind'] == 'query':
            return Query(onetask)
        return onetask
    #def
#class

