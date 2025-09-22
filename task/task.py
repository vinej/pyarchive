from output.util import get_dict_value
import logging
from message.message import gmsg
from task.array import Array
from task.csv import Csv
from task.query import Query
from task.sync import Sync
from task.dir import Dir
from task.log import Log
from task.create import Create
from task.save import Save
from task.unzip import Unzip
from task.curl import Curl
from task.gzip import Gzip

'''
    Master object to run all task
    mapmen:     list of memory object
    mapref:     list of reference object not already instantiated
    vtasks:     list of task
    maptask:    map of all tasks

parameter
    data    :    a json object with Tasks object
'''

TASK_REGISTRY = {}

def register_task(kind, cls):
    TASK_REGISTRY[kind.lower()] = cls

register_task('array', Array)
register_task('csv', Csv)
register_task('query', Query)
register_task('sync', Sync)
register_task('dir', Dir)
register_task('log', Log)
register_task('create', Create)
register_task('save', Save)
register_task('unzip', Unzip)
register_task('curl', Curl)
register_task('gzip', Gzip)

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

    def get_task(self, onetask, position):
        kind = get_dict_value(onetask, 'Kind')
        if kind is None:
            logging.fatal(gmsg.get(27), position, onetask.name, 'Kind')
        kind = kind.lower()
        if kind not in TASK_REGISTRY:
            raise Exception("Invalid Kind for a loop :" + kind)
        return TASK_REGISTRY[kind](onetask)

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
#class

