
from output.output import Output
from myodbc.myodbc import Odbc
import copy
from task.util import get_dict_value
import logging
from message.message import gmsg
import sys

'''
The Parameter class is used by the query to create dynamic parameters to the SQL queries

Kind    :   memory    :  means that parameters come from a static list in memory

            reference :  means that parameters come from a source of type 'reference' that contains also parameters

            child     :  means that parameters come from the previous parameter definition, so this one is a child.

Names   :   the list of parameters names taht will be used into the queries separated by comma
Fields  :   the list of fields from a source that will replaced the parameters into the queries
Source  :   the name of the memory object that contains the rows

Example : you want to a run a query with one parameter : always single

'''
class Parameter:
    def __init__(self,data):
        self.kind = get_dict_value(data,'Kind')
        self.names = get_dict_value(data,'Names')
        self.fields = get_dict_value(data,'Fields')
        self.source = get_dict_value(data,'Source')
    #def
#class

'''
The class Query is a powerfull task to execute SQL queries with dynamilsc variables with one to many levels

The properties of the Query json object

Name            :   name of the task
Kind            :   query
Description     :   the description of the task
Connection      :   the connection name to use for the query
Command         :   the SQL command to execute
Output          :   the output type of the query (memory,csv or excel)
File            :   the destination file name if the output is csv or excel
Excluded        :   the list of columns to exclude from the ouput
Anonymized      :   the list of columns to anonymized
Parameters      :   a list of parameter object used to execute the query
'''
class Query:
    def __init__(self, data):
        self.name = get_dict_value(data,'Name')
        self.kind = get_dict_value(data,'Kind')
        self.description = get_dict_value(data,'Description')
        self.connection = get_dict_value(data,'Connection')
        self.command = get_dict_value(data,'Command')
        self.output = get_dict_value(data,'Output')
        if self.output == "excel" or self.output == "csv":
            self.file = get_dict_value(data,'File')
        else:
            self.file = None
        #if
        self.excluded =  get_dict_value(data,'Excluded')
        self.anonymized =  get_dict_value(data,'Anonymized')

        self.parameters = []
        params = get_dict_value(data,'Parameters')
        if params != None:
            for p in params:
                self.parameters.append(Parameter(p))
            #for
        #if
    #def

    # validate the query properties
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

        if self.connection == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Connection')
            sys.exit(27)
        #if
        self.connection = self.connection.lower()

        if self.output == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Output')
            sys.exit(27)
        #if
        self.output = self.output.lower()

        if (self.output == 'excel' or self.output == 'csv') and self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
            sys.exit(27)
        #if

        if len(self.parameters) > 0:
            for p in self.parameters:
                self.validate_parameter(p, mapcon, position)
            #for
        #if
    #def

    # validate parameters' properties
    def validate_parameter(self, param, mapcon, position):
        _ = mapcon # not use here
        if param.kind == None:
            logging.fatal(gmsg.get(32), position, 'Kind')
        #if
        param.kind = param.kind.lower()

        if param.fields == None:
            logging.fatal(gmsg.get(32), position, 'Fields')
            sys.exit(32)
        #if

        if param.names == None:
            logging.fatal(gmsg.get(32), position,  'Names')
            sys.exit(32)
        #if

        if param.source == None:
            logging.fatal(gmsg.get(32), position,  'Source')
            sys.exit(32)
        #if
        param.source = param.source.lower()
    #def

    # run the query
    def run(self, mapmem, mapref, mapcon, position):
        # started
        logging.info(gmsg.get(4), self.kind, self.name)
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            self.run_internal(self, mapmem, mapref, mapcon, position, 0, False)
        #if
        # completed
        logging.info(gmsg.get(3), self.kind, self.name)
    #def

    # run internal is called by a recursive algorith to run the current queries
    # and save the result unto memory of into a file (csv,excel)
    def run_internal(self, query, mapmem, mapref, mapcon, position, skip, isSkip):
        _ = position # not use for now
        # get the connection to run the query
        connection = mapcon.get_con(query.connection).connection

        # if no parameters, so run the queqry and save the result in memory of into a file
        if len(query.parameters) == 0:
            # run the query
            m = Odbc().run(connection, query.command, query.file, query.name, query.excluded, query.anonymized, query.output)
            # put the result in memory of save it into a file
            if query.output == 'memory' :
                mapmem[query.name] = m
            else:
                if m != None:
                    Output().save(m, query.file, query.name, query.excluded, query.anonymized, query.output)
                #if
            #if
            return True
        else:
            # there are parameters, so run recursively, to execute one to many queries depending of the parameters' list
            return self.run_recursive(mapcon, mapmem, mapref, query.command, query.file, query, 0, None, skip, isSkip)
        #if
    #def

    # name quote for Cvs
    def adjust_quote(self,value):
        if value[0] == '\'' and value[1] != '\'':
            value = value[1:]
        #if
        if value[len(value)-1] == '\'' and value[len(value)-2] != '\'':
            value = value[:len(value)-1]
        #if
        value = value.replace("''", "'")
        return value
    #def

    # adjust quote for parameters
    def adjust_cmd_all(self, cmd, param, row):
        for i in range(len(param.fields)):
            paramvalue = self.adjust_quote(str(row[param.fields[i]]))
            cmd = cmd.replace(param.names[i], paramvalue)
        #for
        return cmd
    #def

    # generate a dynamic file output depending of the current parameters
    def adjust_cmd_out_index(self,cmd, file, param, row, index):
        paramvalue = self.adjust_quote(str(row[param.fields[index]]))
        cmd = cmd.replace(param.names[index], paramvalue.strip())
        if file != None:
            path = file.split('.')
            file = path[0] + "_p" + paramvalue.strip() + '.' + path[1]
        #if
        return (cmd, file)
    #def

    # run the query for all parameters that could be memory,reference or child
    # con       :   the connection to use
    # mapmem    :   the map of all data in memory, could be used of param.Kind = 'memory'
    # mapref    :   all the task of type 'reference' because they are executed with parameters. use for param.Kind = 'reference'
    # cmd       :   the SQL command to execute
    # file      :   the outpuyt file
    # querytask :   the query task defenition
    # level     :   the recursive level
    # row       :   the current row for child parameters
    # Note: the skip and isSkip is almost a patch to make it work with 3 levels (memory,reference,child)
    #       maybe a bette way to do that.
    # skip      :   the number of record to skip
    # isSkip    :   is the skip is needed
    def run_recursive(self, mapcon, mapmem, mapref, cmd, file, querytask, level, row, skip, isSkip):
        param = querytask.parameters[level]
        # if type of child, parameters must be adjust with the current parent row
        if param.kind == 'child':
            #addust parameters
            self.adjust_cmd_from_parent(mapcon, mapmem, mapref, querytask.parameters[level-1], param, row, skip, isSkip)
            # run men
            return self.run_mem(param, mapcon, mapmem, mapref, cmd, file, querytask, level, skip, isSkip)
        # if type reference, we need a deep copy of the current state and we will run for all rows. 
        # as we don't know the number of rows in advance, we loop max 10M times
        elif param.kind == "reference":
            squery = mapref[param.source]
            tmpquery = copy.deepcopy(squery)
            tmpquery.output = 'memory'
            for i in range(100000000):
                done = self.run_internal(tmpquery, mapmem, mapref, mapcon, 1, i, True)
                if done == False:
                    break
                #if
                self.run_mem(param, mapcon, mapmem, mapref, cmd, file, querytask, level, skip, isSkip)
            #for
            return True
        elif param.kind == "memory":
            return self.run_mem(param, mapcon, mapmem, mapref, cmd, file, querytask, level, skip, isSkip)
        else:
            # not supposed to come here because of the pre-validation
            raise Exception("parameter's kind not implemented") 
    #def

    # run_mem, 
    def run_mem(self, param, mapcon, mapmem, mapref, cmd, file, query, level, skip, isSkip):
        mem = mapmem[param.source]

        # it's here we check the max rows to execute
        # the skip is fast because everything is in memory
        if isSkip and skip >= len(mem.rows):
            #no more reference to do
            return False
        #if

        # skip the record already done, get aslice of the rows
        if isSkip and skip > 0:
            rows = mem.rows[skip:]
        else:
            rows = mem.rows
        #if 

        for r in range(len(rows)):
            tmpcmd = cmd
            tmpfile = file
            for i in range(len(param.fields)):
                if i+1 < len(param.fields) and param.fields[i] == param.fields[i+1] :
                    r = r + 1
                    if r == len(rows):
                        return True  # completed, no more data
                    #if
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, rows[r], i+1)
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, rows[r-1], i)
                else :
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, rows[r], i)
                #if
            #for

            if level == len(query.parameters) - 1:
                if isSkip:
                    self.save_memory(query, tmpcmd, mapcon, mapmem, mapref)
                else:
                    self.save_output(query, tmpcmd, tmpfile, mapcon, mapmem, mapref)
                #if
            else:
                self.run_recursive(mapcon, mapmem, mapref, tmpcmd, tmpfile, query, level+1, rows[r], skip, isSkip)
            #if

            if isSkip:
                return True
            #if
        #for
        return True
    #def
    
    # adjust the sql command with the paramen value (use for the child case)
    def adjust_cmd_from_parent(self, mapcon, mapmem, mapref, p1, p2, row, skip, isSkip):
        query = mapref[p2.source]
        cmd = self.adjust_cmd_all(query.command, p1, row)
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.output = 'memory'
        self.run_internal(querytmp, mapmem, mapref, mapcon, 1, skip, isSkip)
    #def

    # save the result into a file
    def save_output(self, query, cmd, file, mapcon, mapmem, mapref):
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.file = file
        querytmp.parameters = []
        self.run_internal(querytmp, mapmem, mapref, mapcon, 0, 0, False)
    #def

    # save the result in memory
    def save_memory(self, query, cmd, mapcon, mapmem, mapref):
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.output = 'memory'
        querytmp.parameters = []
        self.run_internal(querytmp, mapmem, mapref, mapcon, 0, 0, False)
    #def
#class
