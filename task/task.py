from task.array import Array
from task.csv import Csv
from task.query import Query
from task.save import Save
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
            ct = self.get_task(t, i)
            ct.validate(mapcon, i)
            self.vtasks.append(ct)
            i = i + 1
        #for
    #def

    def get_task(self, onetask, position):
        kind = get_dict_value(onetask, 'Kind')
        if kind == None:
            logging.fatal(gmsg.get(27), position, onetask.name, 'Kind')
        #if
        kind = kind.lower()
        if kind == 'array':
            return Array(onetask)
        elif kind == 'csv':
            return Csv(onetask)
        elif kind == 'query':
            return Query(onetask)
        elif kind == "save":
            return Save(onetask)
        #if
        return onetask
    #def
#class

