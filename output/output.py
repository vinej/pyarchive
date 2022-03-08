from pandas import DataFrame
from output.anonymize import Anonymized
from task.memory import Memory
from output.anonymize import ano

'''
simple class to encapsulate the output algo

'''
class Output:
    def save(self, memory, file, name, excluded, anonymized, output):
        df = DataFrame(memory.rows)
        df.index.name="#"
        if len(memory.rows) > 0:
            # remove excluded columns
            if excluded != None:
                for column in excluded:
                    if column in df.columns:
                        del df[column]
                    #if
                #for
            #if

            # anonymized columns
            if anonymized != None:
                for column in anonymized:
                    if column in df.columns:
                        # for each value of the columsn, put the anonimez value
                        for c in range(len(df)):
                            value = df[column][c]
                            df[column][c] = ano.anonymized(name, column, value)
                        pass
                    #if
                #for
            #for
        #if

        if output == "excel":
            df.to_excel(file)
        else:
            df.to_csv(file)
        #if
    #def
#class
