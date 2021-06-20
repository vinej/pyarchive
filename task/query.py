
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
        else:
            self.file = None
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
            self.run_internal(self, mapmem, mapref, con, position, 0, False)
        #if
    #def

    def run_internal(self, query, mapmem, mapref, con, position, skip, isSkip):
        _ = position # not use for now
        connection = con.get_con(query.connection).connection
        if len(query.parameters) == 0:
            m = Odbc().run(connection, query.command)
            if query.output == 'memory' :
                mapmem[query.name] = m
            else:
                Excel().save(m, query.file)
            #if
            return True
        else:
            return self.run_recursive(con, mapmem, mapref, query.command, query.file, query, 0, None, skip, isSkip)
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
        if file != None:
            path = file.split('.')
            file = path[0] + "_p" + paramvalue.strip() + '.' + path[1]
        #if
        return (cmd, file)
    #def

    def run_recursive(self, con, mapmem, mapref, cmd, file, query, level, row, skip, isSkip):
        param = query.parameters[level]
        if param.kind == 'child':
            self.query_reference_parent(con, mapmem, mapref, query.parameters[level-1], param, row, skip, isSkip)
            return self.run_mem(param, con, mapmem, mapref, cmd, file, query, level, skip, isSkip)
        elif param.kind == "multiple":
            squery = mapref[param.source]
            tmpquery = copy.deepcopy(squery)
            tmpquery.output = 'memory'
            for i in range(10000000):
                done = self.run_internal(tmpquery, mapmem, mapref, con, 1, i, True)
                if done == False:
                    break
                #if
                self.run_mem(param, con, mapmem, mapref, cmd, file, query, level, skip, isSkip)
            #for
            return True
        else:
            return self.run_mem(param, con, mapmem, mapref, cmd, file, query, level, skip, isSkip)
        #if    
    #def

    def run_mem(self, param, con, mapmem, mapref, cmd, file, query, level, skip, isSkip):
        mem = mapmem[param.source]

        if isSkip and skip >= len(mem.rows):
            #no more multiple to do
            return False
        #if
        first = True
        for r in range(len(mem.rows)):
            if isSkip and skip > 0:
                skip = skip - 1
                continue
            #if
            tmpcmd = cmd
            tmpfile = file
            iskip = False
            for i in range(len(param.fields)):
                if iskip:
                    iskip = False
                    continue
                #if
                if i+1 < len(param.fields) and param.fields[i] == param.fields[i+1] :
                    if first :
                        r = r + 1
                        first = False
                    #if
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r], i+1)
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r-1], i)
                    iskip = True
                else :
                    (tmpcmd, tmpfile) = self.adjust_cmd_out_index(tmpcmd, tmpfile, param, mem.rows[r], i)
                #if
            #for

            if level == len(query.parameters) - 1:
                if isSkip:
                    self.save_memory(query, tmpcmd, con, mapmem, mapref)
                else:
                    self.save_output(query, tmpcmd, tmpfile, con, mapmem, mapref)
                #if
            else:
                self.run_recursive(con, mapmem, mapref, tmpcmd, tmpfile, query, level+1, mem.rows[r], skip, isSkip)
            #if

            if isSkip:
                return True
            #if
        #for
        return True
    #def
    
    def query_reference_parent(self, con, mapmem, mapref, p1, p2, row, skip, isSkip):
        query = mapref[p2.source]
        cmd = self.adjust_cmd_all(query.command, p1, row)
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.output = 'memory'
        self.run_internal(querytmp, mapmem, mapref, con, 1, skip, isSkip)
    #def

    def save_output(self, query, cmd, file, con, mapmem, mapref):
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.file = file
        querytmp.parameters = []
        self.run_internal(querytmp, mapmem, mapref, con, 0, 0, False)
    #def

    def save_memory(self, query, cmd, con, mapmem, mapref):
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.output = 'memory'
        querytmp.parameters = []
        self.run_internal(querytmp, mapmem, mapref, con, 0, 0, False)
    #def
#class
