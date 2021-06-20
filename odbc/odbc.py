import pyodbc
from task.memory import Memory

class Odbc:
    def _init__(self):
        pass
    #def

    def run(self, connectionString, query):
        con = pyodbc.connect(connectionString)
        cursor = con.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = []
        row = cursor.fetchone()
        while row:
            rows.append(dict(zip(columns, row)))
            row = cursor.fetchone()
        #while
        return Memory(columns, rows)
    #def
#class