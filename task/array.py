from task.memory import Memory
from excel.excel import Excel
from task.util import get_dict_value

class Array:
    def __init__(self, data):
        self.name = get_dict_value(data,'Name').lower()
        self.kind = get_dict_value(data,'Kind').lower()
        self.description = get_dict_value(data,'Description')
        self.command = get_dict_value(data,'Command')
        self.outputtype = get_dict_value(data,"OutputType").lower()
        if self.outputtype == "excel" or self.outputtype == "csv":
            self.fileName = get_dict_value(data,'FileName')
        #if
    #def

    def run(self, mapmem, mapref, con, position):
        if self.outputtype == 'reference':
            mapref[self.name] = self
        else:
            _ = con    # not used for now
            _ = position  # not used for now
            _ = mapref # not used for now
            columns = [self.name]
            arows = self.command.split('|')
            rows = []
            for value in arows:
                onerow = {}
                onerow[self.name] = value
                rows.append(onerow)
            #
            m = Memory(columns, rows)
            if self.outputtype == "excel":
                Excel().save(m, self.fileName)
            else :
                mapmem[self.name] = m
            #if
        #if
    #def
#class

