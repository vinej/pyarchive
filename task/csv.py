from task.memory import Memory
import csv
from excel.excel import Excel
from task.util import get_dict_value

class Csv:
    def __init__(self, data):
        self.name =  get_dict_value(data,'Name').lower()
        self.kind =  get_dict_value(data,'Kind').lower()
        self.description =  get_dict_value(data,'Description')
        self.filename =  get_dict_value(data, 'FileName')
        self.outputtype =  get_dict_value(data, 'OutputType').lower()
        if self.outputtype == "excel" or self.outputtype == "csv":
            self.outfilename = get_dict_value(data,'OutFileName')
        #if
    #def

    def run(self, mapmem, mapref, con, position):
        if self.outputtype == 'reference':
            mapref[self.name] = self
        else:
            _ = con    # not used for now
            _ = position  # not used for now
            _ = mapref   # not used for now
            rows = []
            columns = []
            with open(self.filename, mode ='r') as file:
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
            if self.outputtype == "excel":
                Excel().save(m, self.outfilename)
            else :
                mapmem[self.name] = m
            #if
        #if
    #def
#class