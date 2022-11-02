from output.memory import Memory
from task.array import Array
from task.csv import Csv
from task.query import Query
from task.save import Save
from task.curl import Curl
from output.exceltemplate import ExcelTemplate
from output.util import get_dict_value
import logging
from message.message import gmsg
import json
'''
    Master object to run all task
    mapmen:     list of memory object
    mapref:     list of reference object not already instantiated
    vtasks:     list of task
    maptask:    map of all tasks

parameter
    data    :    a json object with Tasks object
'''
class Loop:
    def __init__(self, jsondata):
        self.mapmem = {}
        self.mapref = {}
        self.vtasks = []
        self.maptask = []
        mapjsontask = jsondata['Loops']
        if mapjsontask is not None:
            for t in mapjsontask:
                self.maptask.append(t)
        #for
    #def

    '''
        run all tasks

        parameter: mapcon a map of all current connections
    '''
    def run(self, mapcon):
        i = 1
        for vt in self.vtasks:
            # the run method is called of the task object
            vt.run(self.mapmem, self.mapref, mapcon, i, None)
            i = i + 1
        #for
    #def

    '''
    Run a task of type reference to update data in memory
    '''
    def run_task(self, mapcon, task, position, g_rows):
        task.run(self.mapmem, self.mapref, mapcon, position, g_rows)
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

    '''
    Create a fixed 5 layers vtask. 
    '''
    def set_layer_mapmem(self, qte):
        count = 1
        jsondata = """ { 
            "Name" : "fake",
            "Kind" : "array",  
            "Description" : "fake",
            "Command" : "fake"
        } """
        while len(self.mapmem) < qte:
            self.mapmem["fake"+str(count)] = Memory( ["fake"], [{"fake": ""}])
            ar = Array(json.loads(jsondata))
            ar.name = ar.name+str(count)
            self.vtasks.append( ar )
            count = count + 1
        #while
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
        elif kind == 'curl':
            return Curl(onetask)
        else:
            raise Exception("Invalid Kind for a GlobalParameter :" + kind)
        #if 
    #def
#class

