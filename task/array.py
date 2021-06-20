from task.memory import Memory
from excel.excel import Excel
from task.util import get_dict_value

class Array:
    def __init__(self, data):
        self.name = get_dict_value(data,'Name').lower()
        self.kind = get_dict_value(data,'Kind').lower()
        self.description = get_dict_value(data,'Description')
        self.command = get_dict_value(data,'Command')
        self.output = get_dict_value(data,"Output").lower()
    #def

    def run(self, mapmem, mapref, con, position):
        if self.output == 'reference':
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
            mapmem[self.name] = m
        #if
    #def
#class

