from task.util import get_dict_value
from task.util import replace_global_parameter
import logging
from message.message import gmsg
from output.output import Output
import sys
'''
The class Save is used to save the data in memory to files with differents options
Name        :   the name of the task
Kind        :   save
Description :   the description of the task
Output      :   csv or excel
Source      :   the name of the source data to save
File        :   contains the file name ouput
Excluded    :   a list of excluded columns
Anonymized  :   a list of columns to anonymized
'''
class Save:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.output = get_dict_value(jsondata,"Output")
        self.file = get_dict_value(jsondata,"File")
        self.source = get_dict_value(jsondata,"Source")
        self.excluded = get_dict_value(jsondata,"Excluded")
        self.anonymized = get_dict_value(jsondata,"Anonymized")
    #def

    def validate(self, mapcon, position):  
        _ = mapcon # not use here
        if self.name == None:
            logging.fatal(gmsg.get(26), position, 'Name')
            sys.exit(26)
        #if
        self.name = self.name.lower()

        if self.kind == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Kind')
            sys.exit(27)
        #
        self.kind = self.kind.lower()

        if self.output == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Output')
            sys.exit(27)
        #if
        self.output = self.output.lower()

        if self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
            sys.exit(27)
        #if

        if self.source == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Source')
            sys.exit(27)
        #if
        self.source = self.source.lower()

        if self.output != 'excel' and self.output != "csv":
            logging.errro(gmsg.get(28), position, self.name, 'Output')
            logging.fatal(gmsg.get(29))
            sys.exit(28)

        #if
	#def

    def run(self, mapmem, mapref, con, position, g_row):
        _ = con    # not used for now
        _ = position  # not used for now
        _ = mapref # not used for now
        
                # adjust global parameters
        self.file = replace_global_parameter(self.file, g_row)
        self.description = replace_global_parameter(self.description, g_row)
        self.output = replace_global_parameter(self.output, g_row)
        self.excluded = replace_global_parameter(self.excluded, g_row)
        self.anonymized = replace_global_parameter(self.anonymized, g_row)
        # started
        logging.info(gmsg.get(4), self.kind, self.name)
        # get the object to save into a file
        m = mapmem[self.source]
        if m != None:
            Output().save(m, self.file, self.name, self.excluded, self.anonymized, self.output)
        #if
        # completed
        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

