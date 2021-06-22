import pyodbc
from task.memory import Memory
import logging
from message.message import gmsg

class Odbc:
    def _init__(self):
        pass
    #def

    def run(self, connection, query):
        logging.info(gmsg.get(8), query)
        con = pyodbc.connect(connection)
        cursor = con.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = []
        row = cursor.fetchone()
        while row:
            rows.append(dict(zip(columns, row)))
            row = cursor.fetchone()
        #while
        logging.info(gmsg.get(9), query)
        return Memory(columns, rows)
    #def
#class