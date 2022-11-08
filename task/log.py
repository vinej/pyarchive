from output.memory import Memory
from myodbc.myodbc import Odbc
from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys

'''
The Create class is used to create a simple a table from a list of definition

The json object properties

'''
class Log:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.file = get_dict_value(jsondata,'File')
        self.unique = get_dict_value(jsondata,'Unique')
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

        if self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
            sys.exit(27)
        #if
        self.file = self.file.lower()

        if self.unique == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Unique')
            sys.exit(27)
        #if
        self.unique = self.unique.lower()
	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position
        _ = mapref

        self.description = replace_global_parameter(self.description, g_rows)
        self.file = replace_global_parameter(self.file, g_rows)
        # read the directory

        rows = []
        dict = {}
        if self.unique == 'true' :
            columns = ["date","user"]
        else:
            columns = ["date","url","user"]

        for line in open(self.file).readlines():
            sline = str(line)
            if sline[0] == "#":
                continue
                
            aline = sline.split(" ")

            user = aline[9]
            date = aline[0]
            time = aline[1]
            url = aline[6]

            if user == "-" : # no user
                continue

            if self.unique == "true":
                if not user+date in dict:
                    onerow = {}
                    onerow["date"] = date
                    onerow["user"] = user
                    rows.append(onerow)  
                    dict[user+date] = ''
            else :
                onerow = {}
                onerow["date"] = date + " " + time
                onerow["url"] = url
                onerow["user"] = user
                rows.append(onerow)
        #
        m = Memory(columns, rows)
        mapmem[self.name] = m

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

