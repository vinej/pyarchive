from output.memory import Memory
from myodbc.myodbc import Odbc
from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys
import glob

from task.base import BaseTask

'''
The Dir class is used to read in memory files contain into a directory (with sub dir if recursive = true)

The json object properties

Name            :   name of the task
Kind            :   query
Description     :   the description of the task
path            :   the path to read, can contains pattern like *.log
recursive       :   true/false to read sub directories
'''
class Dir(BaseTask):
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.path = get_dict_value(jsondata,'Path')
        self.recursive = get_dict_value(jsondata,'Recursive')
    #def

    def validate(self, mapcon, position):  
        _ = mapcon # not use here
        if self.name == None:
            logging.fatal(gmsg.get(26), position, 'Name')
            sys.exit(26)
        #if
        self.name = self.name.lower()

        if self.kind == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Kind')
            sys.exit(27)
        #
        self.kind = self.kind.lower()

        if self.description == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Description')
            sys.exit(27)
        #if

        if self.path == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Path')
            sys.exit(27)
        #if
        self.path = self.path.lower() 

        if self.recursive == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Recursive')
            sys.exit(27)
        #if
        self.recursive = self.recursive.lower() 
	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position
        _ = mapref

        self.description = replace_global_parameter(self.description, g_rows)
        self.path = replace_global_parameter(self.path, g_rows)
        self.recursive = replace_global_parameter(self.recursive, g_rows)

        isRecurse = False
        if self.recursive == "true" :
            isRecurse = True

        columns = ["file"]
        rows = []
        for path in glob.glob(self.path, recursive=isRecurse):
            onerow = {}
            onerow["file"] = path
            rows.append(onerow)
        #
        m = Memory(columns, rows)
        mapmem[self.name] = m

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

