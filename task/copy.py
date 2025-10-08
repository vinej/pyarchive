import os
import shutil
import time


from output.memory import Memory
import csv
from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys

from task.base import BaseTask

'''
The Csv class is used to read csv file into memory

The json object properties

Name          :   the name of the task
Kind          :   csv
Description   :   the description of the task
Source  :   the source folder for the copy
Destination : the destination folder for the copy
Pattern     : pattern of files to copy : ex *.zip
'''
class Copy(BaseTask):
    def __init__(self, jsondata):
        self.name =  get_dict_value(jsondata,'Name')
        self.kind =  get_dict_value(jsondata,'Kind')
        self.description =  get_dict_value(jsondata,'Description')
        self.source =  get_dict_value(jsondata, 'Source')
        self.destination =  get_dict_value(jsondata, 'Destination')
        self.pattern =  get_dict_value(jsondata, 'Pattern')
    #def

    # run the Csv task
    def run(self, mapmem, mapref, mapcon, position, g_rows):
        # replace the global parameter

        self.source = replace_global_parameter(self.source, g_rows)
        self.destination = replace_global_parameter(self.destination, g_rows)

        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = position  # not used for now
        _ = mapref   # not used for now

        os.makedirs(self.destination, exist_ok=True)

        # List all files in the source folder
        files = [f for f in os.listdir(self.source) if os.path.isfile(os.path.join(self.source, f))]

        for file_name in files:
            source_path = os.path.join(self.source, file_name)
            destination_path = os.path.join(self.destination, file_name)

            # Copy the file
            shutil.copy2(source_path, destination_path)
            logging.info(gmsg.get(3), self.kind,  self.name)
            print(f"Copied: {file_name}")

            # Optional delay between copies
            time.sleep(1)
        #for

        logging.info(gmsg.get(3), self.kind,  self.name)
    #def

    # validate the Csv task
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

        if self.source == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Source')
            sys.exit(27)
        #if

        if self.destination == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Destination')
            sys.exit(27)
        #if

        if self.pattern == None:
            logging.errro(gmsg.get(27), position, self.name, 'Pattern')

            sys.exit(28)
        #if
	#def
#class
