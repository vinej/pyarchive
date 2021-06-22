from task.memory import Memory
from excel.excel import Excel
from task.util import get_dict_value
import logging
from message.message import gmsg

class Array:
    def __init__(self, data):
        self.name = get_dict_value(data,'Name')
        self.kind = get_dict_value(data,'Kind')
        self.description = get_dict_value(data,'Description')
        self.command = get_dict_value(data,'Command')
        self.output = get_dict_value(data,"Output")
    #def

    def validate(self, mapcon, position):  
        _ = mapcon # not use here
        if self.name == None:
            logging.fatal(gmsg.get(26), position, 'Name')
        #if
        self.name = self.name.lower()

        if self.kind == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Kind')
        #
        self.kind = self.kind.lower()

        if self.command == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Command')
        #if

        if self.output == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Output')
        #if
        self.output = self.output.lower()

        if self.output != 'memory':
            logging.errro(gmsg.get(28), position, self.name, 'Output')
            logging.fatal(gmsg.get(29))
        #if
	#def

    def run(self, mapmem, mapref, con, position):
        logging.info(gmsg.get(4), self.kind, self.name)
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            _ = con    # not used for now
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

