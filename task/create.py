from output.memory import Memory
from myodbc.myodbc import Odbc
from output.util import get_dict_value
import logging
from message.message import gmsg
import sys

'''
The Create class is used to create a simple a table from a list of definition

The json object properties

Name        :   the name of the task
Kind        :   create
Description :   the description of the task
Source      :   the list of definition to use
Connection  :   connection to create the table
'''
class Create:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.source = get_dict_value(jsondata,'Source')
        self.connection = get_dict_value(jsondata,'Connection')
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

        if self.source == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Source')
            sys.exit(27)
        #if
        self.source = self.source.lower()

        if self.connection == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Connection')
            sys.exit(27)
        #if
        self.connection = self.connection.lower()   
	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position

        if len(mapmem[self.source].rows) == 0 :
            return

        sql = "CREATE TABLE "
        isFirst = True
        for row in mapmem[self.source].rows :

            if  isFirst == False:
                sql = sql + ","
            else :
                sql = sql + row["TABLE_NAME"] + "("

            sql = sql + row["COLUMN_NAME"] + " " + row["DATA_TYPE"]
            if row["DATA_TYPE"] == "varchar" or row["DATA_TYPE"] == "char":
                sql = sql + "(" + str(row["CHARACTER_MAXIMUM_LENGTH"]) + ")"
            elif row["DATA_TYPE"] == "nvarchar" :
                sql = sql + "(" + str(row["CHARACTER_MAXIMUM_LENGTH"]*2) + ")"
            isFirst = False
        sql = sql +");"
        # get the connection to run the query
        connection = mapcon.get_con(self.connection).connection

        Odbc().run(connection, sql, None, None, None, None, "ddl")
    #def
#class

