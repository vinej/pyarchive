from task.memory import Memory
import csv
from task.util import get_dict_value
import logging
from message.message import gmsg
import logging
from message.message import gmsg
import sys

'''
The Csv class is used to read csv file

The json object propertiesw

Name        :   the name of the task
Kind        :   csv
Description :   the description of the task
File        :   the input csv file
Output      :   memory or reference
'''
class Csv:
    def __init__(self, jsondata):
        self.name =  get_dict_value(jsondata,'Name')
        self.kind =  get_dict_value(jsondata,'Kind')
        self.description =  get_dict_value(jsondata,'Description')
        self.file =  get_dict_value(jsondata, 'File')
        self.output =  get_dict_value(jsondata, 'Output')
    #def

    # run the Csv task
    def run(self, mapmem, mapref, mapcon, position):
        logging.info(gmsg.get(4), self.kind, self.name)
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            _ = mapcon    # not used for now
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

    # validate the Csv task
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

        if self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
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
    
#class