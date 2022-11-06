from task.array import Array
from task.csv import Csv
from task.query import Query
from task.save import Save
from task.curl import Curl
from task.create import Create
from task.sync import Sync
from output.util import get_dict_value
import logging
from message.message import gmsg
'''
    Master object to run all task
    mapmen:     list of memory object
    mapref:     list of reference object not already instantiated
    vtasks:     list of task
    maptask:    map of all tasks

parameter
    data    :    a json object with Tasks object
'''
class Task:
    def __init__(self, jsondata):
        self.mapmem = {}
        self.mapref = {}
        self.vtasks = []
        self.maptask = []
        mapjsontask = jsondata['Tasks']
        for t in mapjsontask:
            self.maptask.append(t)
        #for
    #def

    '''
        run all tasks

        parameter: mapcon a map of all current connections
    '''
    def run(self, mapcon, g_rows):
        i = 1
        # run all task in a sequential order
        for vt in self.vtasks:
            # the run method is called of the task object
            vt.run(self.mapmem, self.mapref, mapcon, i, g_rows)
            i = i + 1
        #for
    #def

    '''
        validate the tasks information before running
    '''
    def validate(self, mapcon):
        i = 1
        for t in self.maptask:
            # create and get a task object depinding of the kind property
            ct = self.get_task(t, i)
            #validate the task
            ct.validate(mapcon, i)
            # add the task into vtasks list
            self.vtasks.append(ct)
            i = i + 1
        #for
    #def

    # get a specific task a postion x
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
        elif kind == 'sync':
            return Sync(onetask)
        elif kind == 'create':
            return Create(onetask)
        elif kind == "save":
            return Save(onetask)
        elif kind == "curl":
            return Curl(onetask)
        else:
            raise Exception("Invalid Kind for a loop :" + kind)
        #if 
    #def
#class

