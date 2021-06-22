from task.array import Array
from task.csv import Csv
from task.query import Query
from task.util import get_dict_value
import logging
from message.message import gmsg

class Task:
    def __init__(self, data):
        self.mapmem = {}
        self.mapref = {}
        self.vtasks = []
        self.maptask = []
        mapjsontask = data['Tasks']
        for t in mapjsontask:
            self.maptask.append(t)
        #for
    #def

    def run(self, mapcon):
        i = 1
        for vt in self.vtasks:
            vt.run(self.mapmem, self.mapref, mapcon, i)
            i = i + 1
        #for
    #def

    def validate(self, mapcon):
        i = 1
        for t in self.maptask:
            ct = self.get_task(t)
            ct.validate(mapcon, i)
            self.vtasks.append(ct)
            i = i + 1
        #for
    #def

    def get_task(self, onetask):
        kind = get_dict_value(onetask, 'Kind')
        if kind == None:
            logging.fatal(gmsg.get(58))
        #if
        kind = kind.lower()
        if kind == 'array':
            return Array(onetask)
        elif kind == 'csv':
            return Csv(onetask)
        elif kind == 'query':
            return Query(onetask)
        return onetask
    #def
#class

