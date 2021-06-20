
from odbc.odbc import Odbc
from excel.excel import Excel
import copy
from task.util import get_dict_value

class Parameter:
    def __init__(self,data):
        self.kind = get_dict_value(data,'Kind')
        self.names = get_dict_value(data,'Names')
        self.fields = get_dict_value(data,'Fields')
        self.source = get_dict_value(data,'Source')
    #def
#class

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
        #if
        self.parameters = []
        params = get_dict_value(data,'Parameters')
        if params != None:
            for p in params:
                self.parameters.append(Parameter(p))
            #for
        #if
    #def

    def run(self, mapmem, mapref, con, position):
        if self.output == 'reference':
            mapref[self.name] = self
        else:
            self.run_internal(self, mapmem, mapref, con, position)
        #if
    #def

    def run_internal(self, query, mapmem, mapref, con, position):
        connection = con.get_con(query.connection).connection
        if len(query.parameters) == 0:
            m = Odbc().run(connection, query.command)
            if query.output == 'memory' :
                mapmem[query.name] = m
            else:
                Excel().save(m, query.file)
            #if
        else:
            self.run_recursive(con, mapmem, mapref, query.command, query.file, query, 0, None)
        #if
    #def

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

    def adjust_cmd_all(self, cmd, param, row):
	    for i in range(len(param.fields)):
		    paramvalue = self.adjust_quote(str(row[param.fields[i]]))
		    cmd = cmd.replace(param.names[i], paramvalue)
        #for
	    return cmd
    #def

    def adjust_cmd_out_index(self,cmd, file, param, row, index):
        paramvalue = self.adjust_quote(str(row[param.fields[index]]))
        cmd = cmd.replace(param.names[index], paramvalue.strip())
        if file != "":
            path = file.split('.')
            file = path[0] + "_p" + paramvalue.strip() + '.' + path[1]
        #if
        return (cmd, file)
    #def

    def run_recursive(self, con, mapmem, mapref, cmd, file, query, level, row):
        param = query.parameters[level]
        if param.kind == 'child':
            self.query_reference(con, mapmem, mapref, query.parameters[level-1], param, row)
        #if

        mem = mapmem[param.source]

        first = True
        for r in range(len(mem.rows)):
            tmpcmd = cmd
            tmpfile = file
            skip = False
            for i in range(len(param.fields)):
                if skip:
                    skip = False
                    continue
                #if
                if i+1 < len(param.fields) and param.fields[i] == param.fields[i+1] :
                    if first :
                        r = r + 1
                        first = False
                    #if
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r], i+1)
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r-1], i)
                    skip = True
                else :
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r], i)
                #if
            #for

            if level == len(query.parameters) - 1:
                self.save_output(query, tmpcmd, tmpfile, con, mapmem, mapref)
            else:
                self.run_recursive(con, mapmem, mapref, tmpcmd, tmpfile, query, level+1, mem.rows[r])
            #if
        #for
    #def
    
    def query_reference(self, con, mapmem, mapref, p1, p2, row):
        query = mapref[p2.source]
        cmd = self.adjust_cmd_all(query.command, p1, row)
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.output = 'memory'
        self.run_internal(querytmp, mapmem, mapref, con, 1)
    #def

    def save_output(self, query, cmd, file, con, mapmem, mapref):
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.file = file
        querytmp.parameters = []
        self.run_internal(querytmp, mapmem, mapref, con, 0)
    #def
#class
