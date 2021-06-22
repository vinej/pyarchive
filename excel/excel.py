from pandas import DataFrame
from task.memory import Memory

class Excel:
    def save(self, memory, output, excluded, anonymized):
        df = DataFrame(memory.rows)
        if len(memory.rows) > 0:
            if excluded != None:
                for exclude in excluded:
                    if exclude in df.columns:
                        del df[exclude]
                    #if
                #for
            #if
        #if
        for anonymize in anonymized:
            pass
        #for
        df.to_excel(output)
    #def
#class
