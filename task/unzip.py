from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys
from zipfile import ZipFile

'''
The Unzip class is used to unzip a zip into a diurectory

The json object properties
Name            :   name of the task
Kind            :   query
Description     :   the description of the task
File            :   the input file to unzip
Directory       :   destination directory to unzip files
'''
class Unzip:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.file = get_dict_value(jsondata,'File')
        self.directory = get_dict_value(jsondata,'Directory')
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

        if self.description == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Description')
            sys.exit(27)
        #if

        if self.file == None:
            logging.fatal(gmsg.get(27), position, self.name, 'File')
            sys.exit(27)
        #if
        self.file = self.file.lower()

        if self.directory == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Directory')
            sys.exit(27)
        #if
        self.directory = self.directory.lower()
	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = g_rows
        _ = position
        _ = mapref
        _ = mapmem

        self.description = replace_global_parameter(self.description, g_rows)
        self.file = replace_global_parameter(self.file, g_rows)
        self.directory = replace_global_parameter(self.directory, g_rows)
        # read the directory

        # loading the temp.zip and creating a zip object
        with ZipFile(self.file, 'r') as zObject:
            zObject.extractall(path=self.directory)

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

