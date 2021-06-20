from task.memory import Memory
import csv
from excel.excel import Excel
from task.util import get_dict_value

class Csv:
    def __init__(self, data):
        self.name =  get_dict_value(data,'Name').lower()
        self.kind =  get_dict_value(data,'Kind').lower()
        self.description =  get_dict_value(data,'Description')
        self.file =  get_dict_value(data, 'File')
        self.output =  get_dict_value(data, 'Output').lower()
    #def

    def run(self, mapmem, mapref, con, position):
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
    #def
#class