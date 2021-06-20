from pandas import DataFrame
from task.memory import Memory

class Excel:
    def save(self, memory, output):
        df = DataFrame(memory.rows)
        df.to_excel(output)
    #def
#class
