import pyodbc
from task.memory import Memory
import logging
import csv
from message.message import gmsg
from output.anonymize import ano

class Odbc:
    def _init__(self):
        pass
    #def

    def run(self, connection, query, file, name, excluded, anonymized, output):
        if output == 'csv' :
            return self.run_with_direct_output(connection, query, file, name, excluded, anonymized)
        else:
            return self.run_on_memory(connection, query)
        #if
    #def

    def run_on_memory(self, connection, query):
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

    def exclude(self, columns, excluded):
        #remove all excluded from columns
        for column in excluded:
            columns.remove(column)
        #if
        return columns
    #def

    def get_indexes(self, columns, excluded):
        indexes = []
        for column in excluded:
            indexes.append(columns.index(column))
        #for
        return indexes
    #def

    def exclude_index(self, columns, indexes):
        # reverse the array
        #remove all excluded from columns
        indexes.sort(reverse = True)
        for idx in indexes:
            columns.pop(idx)
        #if
        return columns
    #def

    def anonymize(self, columns, anonymized, indexes, name):
        i = 0
        for idx in indexes:
            columns[idx] = ano.anonymized(name, anonymized[i], columns[idx])
            i = i + 1
        #if
        return columns
    #def

    def run_with_direct_output(self, connection, query, file, name, excluded, anonymized):
        logging.info(gmsg.get(8), query)
        with open(file, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)

            con = pyodbc.connect(connection)
            cursor = con.cursor()
            cursor.execute(query)
            ori_columns = [column[0] for column in cursor.description]
            
            columns = [column[0] for column in cursor.description]
            #excluded columns
            if anonymized != None:
                indexes_anonymized = self.get_indexes(columns, anonymized)
            #if
            
            if excluded != None:
                indexes_exclude = self.get_indexes(columns, excluded)
                columns = self.exclude(columns, excluded)
            #f
            csv_writer.writerow(columns)

            row = cursor.fetchone()
            while row:
                if row != None:
                    cols = list(dict(zip(ori_columns, row)).values())
                    if anonymized != None:
                        cols = self.anonymize(cols, anonymized, indexes_anonymized, name)
                    #if
                    if excluded != None:
                        cols = self.exclude_index(cols, indexes_exclude)
                    #if

                    csv_writer.writerow(cols)
                    row = cursor.fetchone()
                #if
            #while
            logging.info(gmsg.get(9), query)
        #with
        return None
    #def
#class