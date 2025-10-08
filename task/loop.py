from output.memory import Memory
from task.array import Array
from task.task import TASK_REGISTRY, Task

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
    jsondata    :    a json object with Tasks object
'''
class Loop(Task):
    def __init__(self, jsondata):
        super().__init__({'Tasks': jsondata['Loops'] if 'Loops' in jsondata and jsondata['Loops'] is not None else []})

    def run(self, mapcon):
        i = 1
        for vt in self.vtasks:
            vt.run(self.mapmem, self.mapref, mapcon, i, None)
            i += 1

    def run_task(self, mapcon, task, position, g_rows):
        task.run(self.mapmem, self.mapref, mapcon, position, g_rows)

    def set_layer_mapmem(self, qte):
        count = 1
        jsondata = """{
            "Name": "fake",
            "Kind": "array",
            "Description": "fake",
            "Command": "fake"
        }"""
        while len(self.mapmem) < qte:
            self.mapmem["fake" + str(count)] = Memory(["fake"], [{"fake": ""}])
            #ar = self.kind_map['array'](json.loads(jsondata))
            #ar = self.get_task('array', 1)(json.loads(jsondata))
            ar = Array(json.loads(jsondata))
            #ar = self.get_task(Array, 1)
            ar.name = ar.name + str(count)
            self.vtasks.append(ar)
            count += 1
#class

