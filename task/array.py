from output.memory import Memory
from output.util import get_dict_value, replace_global_parameter
import logging
from message.message import gmsg
from task.base import BaseTask
import sys

'''
The Array class is used to create a simple array of scalar values in memory

The json object properties

Name        :   the name of the task
Kind        :   array
Description :   the description of the task
Command     :   contains the list of values separated by a pipe |
                or the file name if type = file is used. One value per line.
Type        :   pipe (default), file
'''
class Array(BaseTask):
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.command = get_dict_value(jsondata,'Command')
        self.type = get_dict_value(jsondata,'Type')
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

        if self.type == None:
            self.type = 'pipe'
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

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        
        self.description = replace_global_parameter(self.description, g_rows)
        self.command = replace_global_parameter(self.command, g_rows)
        self.output = replace_global_parameter(self.output, g_rows)
        self.type = replace_global_parameter(self.type, g_rows)

        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = position  # not used for now
        _ = mapref # not used for now
        _ = g_rows
        columns = [self.name]

        if self.type.lower() == 'file':
            try:
                rows = []
                with open(self.command, 'r', encoding='utf-8') as f:
                    for line in f:
                        linestrip = line.strip()
                        if linestrip:  # Avoid empty lines
                            onerow = {}
                            onerow[self.name] = linestrip
                            rows.append(onerow)
                    #for
                #with
                m = Memory(columns, rows)
                mapmem[self.name] = m
            except Exception as e:
                logging.fatal(gmsg.get(30), self.command, str(e))
                sys.exit(30)
            #try
        else: #pipe
            arows = self.command.split('|')
            rows = []
            for value in arows:
                onerow = {}
                onerow[self.name] = value
                rows.append(onerow)
            #for
            m = Memory(columns, rows)
            mapmem[self.name] = m
        #if

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

