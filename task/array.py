from task.memory import Memory
from task.util import get_dict_value
import logging
from message.message import gmsg
import sys

'''
The Array class is used to creat a simple array of scalar value in memory

The json object propertiesw

Name        :   the name of the task
Kind        :   array
Description :   the description of the task
Command     :   contains the list of values separated by a pipe |
Output      :   memory or reference
'''
class Array:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.command = get_dict_value(jsondata,'Command')
        self.output = 'memory'
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

        if self.command == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Command')
            sys.exit(27)
        #if

        if self.output == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Output')
            sys.exit(27)
        #if
        self.output = self.output.lower()

        if self.output != 'memory' and self.output != 'reference':
            logging.errro(gmsg.get(28), position, self.name, 'Output')
            logging.fatal(gmsg.get(29))
            sys.exit(28)
        #if
	#def

    def run(self, mapmem, mapref, mapcon, position):
        logging.info(gmsg.get(4), self.kind, self.name)
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            _ = mapcon    # not used for now
            _ = position  # not used for now
            _ = mapref # not used for now
            columns = [self.name]
            arows = self.command.split('|')
            rows = []
            for value in arows:
                onerow = {}
                onerow[self.name] = value
                rows.append(onerow)
            #
            m = Memory(columns, rows)
            mapmem[self.name] = m
        #if
        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

