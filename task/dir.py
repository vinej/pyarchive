from output.memory import Memory
from myodbc.myodbc import Odbc
from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys
import glob

'''
The Create class is used to create a simple a table from a list of definition

The json object properties

'''
class Dir:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.path = get_dict_value(jsondata,'Path')
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

	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position
        self.description = replace_global_parameter(self.description, g_rows)
        self.path = replace_global_parameter(self.path, g_rows)

        columns = ["file"]
        rows = []
        for path in glob.glob(self.path, recursive=False):
            onerow = {}
            onerow["file"] = path
            rows.append(onerow)
        #
        m = Memory(columns, rows)
        mapmem[self.name] = m

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

