from output.memory import Memory
from myodbc.myodbc import Odbc
from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys

from task.base import BaseTask

'''
The Sync class synchronize 2 table/view from a source table/view with a dest table/view
The json object properties
Name            :   the name of the task
kind            :   the kind of the task
description     :   the description of the task 
sourcetable     :   the source table used to sync with the synctable
synctable       :   the table that will be syncked wit the source table
connection      :   the connection use to access the source and sync tables (use synonyms and link servers if both are not from the same database)
filesync        :   the file that contains the last sync date
createdate      :   the field used as creation date to insert new records
updatedate      :   the field used as last update date to update records
primarykey      :   the primary key fo the sync table
source          :   the mem source that contain the colum definition of the source table
'''
class Sync(BaseTask):
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.sourcetable = get_dict_value(jsondata,'SourceTable')
        self.synctable = get_dict_value(jsondata,'SyncTable')
        self.connection = get_dict_value(jsondata,'Connection')
        self.filesync = get_dict_value(jsondata,'FileSync')
        self.createdate = get_dict_value(jsondata,'CreateDate')
        self.updatedate = get_dict_value(jsondata,'UpdateDate')
        self.primarykey = get_dict_value(jsondata,'PrimaryKey')
        self.source = get_dict_value(jsondata,'Source')
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

        if self.sourcetable == None:
            logging.fatal(gmsg.get(27), position, self.name, 'SourceTable')
            sys.exit(27)
        #if
        self.sourcetable = self.sourcetable.lower()

        if self.synctable == None:
            logging.fatal(gmsg.get(27), position, self.name, 'SyncTable')
            sys.exit(27)
        #if
        self.synctable = self.synctable.lower()

        if self.connection == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Connection')
            sys.exit(27)
        #if
        self.connection = self.connection.lower()    

        if self.filesync == None:
            logging.fatal(gmsg.get(27), position, self.name, 'FileSync')
            sys.exit(27)
        #if
        self.filesync = self.filesync.lower()          

        if self.createdate == None:
            logging.fatal(gmsg.get(27), position, self.name, 'CreateDate')
            sys.exit(27)
        #if
        self.createdate = self.createdate.lower()     

        if self.updatedate == None:
            logging.fatal(gmsg.get(27), position, self.name, 'UpdateDate')
            sys.exit(27)
        #if
        self.updatedate = self.updatedate.lower()  
	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position

        self.sourcetable = replace_global_parameter(self.sourcetable, g_rows)
        self.synctable = replace_global_parameter(self.synctable, g_rows)
        self.connection = replace_global_parameter(self.connection, g_rows)
        self.filesync = replace_global_parameter(self.filesync, g_rows)
        self.createdate = replace_global_parameter(self.createdate, g_rows)
        self.updatedate = replace_global_parameter(self.updatedate, g_rows)
        self.primarykey = replace_global_parameter(self.primarykey, g_rows)
        self.source = replace_global_parameter(self.source, g_rows)

        # get new records
        syncdate = str(open(self.filesync).readline())



        sqlDeleteForInsert = f"delete from {self.synctable} where {self.createdate} > '{syncdate}' "
        sqlSelectForInsert = f"insert into {self.synctable} select * from [[synonyms.synonym_name]] where {self.createdate} > '{syncdate}'"
        sqlSelectForInsert = replace_global_parameter(sqlSelectForInsert, g_rows)

        connection = mapcon.get_con(self.connection).connection
        m = Odbc().run(connection, sqlDeleteForInsert, None, None, None, None, "ddl")
        m = Odbc().run(connection, sqlSelectForInsert, None, None, None, None, "ddl")

        # build the tempate that will be used to update rows
        sql = F"UPDATE {self.synctable} set "
        isFirst = True
        for row in mapmem[self.source].rows :

            if  isFirst == False:
                sql = sql + ","

            sql = sql + row["COLUMN_NAME"] + " = "
            dtype = row["DATA_TYPE"]

            if dtype == "varchar" or dtype == "char" or dtype == "nvarchar" or dtype == "datetime" or dtype == "date":
                sql = sql + "'{{zzz"+row["COLUMN_NAME"]+"}}'"
            else :
                sql = sql + "{{zzz"+row["COLUMN_NAME"]+"}}"
            isFirst = False
        sql = sql + " WHERE {{primarykey}} = " + "{{primarykeyvalue}}"
        templateSql = sql

        # with this sql, go throung all rows that must be updated
        sqlSelect = f"select * from {self.sourcetable} where {self.updatedate} > '{syncdate}'"
        m = Odbc().run(connection, sqlSelect, None, None, None, None, "memory")

        if len(m.rows) > 0:
            for row in m.rows :
                isFirst = True
                sql = templateSql
                primaryKey = self.primarykey
                primaryKeyValue = ""
                for col in m.col :

                    # if the primarykey is not set, take the first col
                    if isFirst == True :
                        if primaryKey == "":
                            primaryKey = col
                        isFirst = False
                    
                    # set the primary key if we found the column
                    if primaryKey == col:
                        primaryKeyValue = str(row[col])

                    if row[col] == None:
                        sql = sql.replace("'{{zzz"+col+"}}'", 'null')   # for string
                        sql = sql.replace("{{zzz"+col+"}}", 'null')   # for number if it was not a string
                    elif row[col] == False:
                        sql = sql.replace("'{{zzz"+col+"}}'", '0')  # for string
                        sql = sql.replace("{{zzz"+col+"}}", '0')   # for number if it was not a string
                    elif row[col] == True:
                        sql = sql.replace("'{{zzz"+col+"}}'", '1')   #for string 
                        sql = sql.replace("{{zzz"+col+"}}", '1')   # for number if it was not a string                         
                    else :
                        value =  str(row[col])
                        value = value.replace("'","''")  # double single quot
                        value = value.replace('"','""')  # double double quot
                        # date,guid are managed like string
                        sql = sql.replace("{{zzz"+col+"}}", str(row[col]))
                        
                #for
                sql = sql.replace("{{primarykey}}", primaryKey)
                sql = sql.replace("{{primarykeyvalue}}", primaryKeyValue)
                m = Odbc().run(connection, sql, None, None, None, None, "ddl")
    #def
#class :

