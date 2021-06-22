from task.memory import Memory
import csv
from excel.excel import Excel
from task.util import get_dict_value
import logging
from message.message import gmsg
import logging
from message.message import gmsg

class Csv:
    def __init__(self, data):
        self.name =  get_dict_value(data,'Name')
        self.kind =  get_dict_value(data,'Kind')
        self.description =  get_dict_value(data,'Description')
        self.file =  get_dict_value(data, 'File')
        self.output =  get_dict_value(data, 'Output')
    #def

    def run(self, mapmem, mapref, con, position):
        logging.info(gmsg.get(4), self.kind, self.name)
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            _ = con    # not used for now
            _ = position  # not used for now
            _ = mapref   # not used for now
            rows = []
            columns = []
            with open(self.file, mode ='r') as file:
                # reading the CSV file
                csvFile = csv.reader(file)
    
                # displaying the contents of the CSV file
                first = True
                for row in csvFile:
                    if first:
                        columns = row
                        first = False
                    else :
                        onerow = {}
                        for i in range(len(columns)):
                            onerow[columns[i]] = row[i]
                        #for
                        rows.append(onerow)
                    #if
                #
            #with
            m = Memory(columns, rows)
            mapmem[self.name] = m
        #if
        logging.info(gmsg.get(3), self.kind,  self.name)
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

        if self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
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
    
#class