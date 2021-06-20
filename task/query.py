
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
        self.outputtype = get_dict_value(data,'OutputType')
        if self.outputtype == "excel" or self.outputtype == "csv":
            self.filename = get_dict_value(data,'FileName')
        else:
            self.filename = ""
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
        if self.outputtype == 'reference':
            mapref[self.name] = self
        else:
            self.run_internal(self, mapmem, mapref, con, position)
        #if
    #def

    def run_internal(self, query, mapmem, mapref, con, position):
        connectionString = con.get_con(query.connection).connectionString
        if len(query.parameters) == 0:
            m = Odbc().run(connectionString, query.command)
            if query.outputtype == 'memory' :
                mapmem[query.name] = m
            else:
                Excel().save(m, query.filename)
            #if
        else:
            self.run_recursive(con, mapmem, mapref, query.command, query.filename, query, 0, None)
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

    def adjust_cmd_out_index(self,cmd, output, param, row, index):
        paramvalue = self.adjust_quote(str(row[param.fields[index]]))
        cmd = cmd.replace(param.names[index], paramvalue.strip())
        if output != "":
            path = output.split('.')
            output = path[0] + "_p" + paramvalue.strip() + '.' + path[1]
        #if
        return (cmd, output)
    #def

    def run_recursive(self, con, mapmem, mapref, cmd, output, query, level, row):
        param = query.parameters[level]
        if param.kind == 'child':
            self.query_task(con, mapmem, mapref, query.parameters[level-1], param, row)
            mem = mapmem[param.source]
            self.run_mem(mem, con, mapmem, mapref, cmd, output, query, level, row)
        elif param.kind == 'multiple':
            pass
        else:
            mem = mapmem[param.source]
            self.run_mem(mem, con, mapmem, mapref, cmd, output, query, level, row)
        #if
    #def

    def run_mem(self, mem, param, con, mapmem, mapref, cmd, output, query, level):
        first = True
        for r in range(len(mem.rows)):
            cmd2 = cmd
            output2 = output
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
                    (cmd2, output2) = self.adjust_cmd_out_index(cmd2, output2, param, mem.rows[r], i+1)
                    (cmd2, output2) = self.adjust_cmd_out_index(cmd2, output2, param, mem.rows[r-1], i)
                    skip = True
                else :
                    (cmd2, output2) = self.adjust_cmd_out_index(cmd2, output2, param, mem.rows[r], i)
                #if
            #for

            if level == len(query.parameters) - 1:
                querytmp = copy.deepcopy(query)
                querytmp.command = cmd2
                if output2 != "":
                    querytmp.filename = output2
                else:
                    querytmp.outputtype = 'memory'
                #if
                querytmp.parameters = []
                self.run_internal(querytmp, mapmem, mapref, con, 0)
            else:
                self.run_recursive(con, mapmem, mapref, cmd2, output2, query, level+1, mem.rows[r])
            #if
        #for
    #def
    
    def query_task(self, con, mapmem, mapref, p1, p2, row):
        query = mapref[p2.source]
        cmd = self.adjust_cmd_all(query.command, p1, row)
        querytmp = copy.deepcopy(query)
        querytmp.command = cmd
        querytmp.outputtype = 'memory'
        self.run_internal(querytmp, mapmem, mapref, con, 1)
    #def
#class
