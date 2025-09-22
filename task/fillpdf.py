from output.memory import Memory
from output.util import get_dict_value, replace_global_parameter
import logging
from message.message import gmsg
from task.base import BaseTask
import sys
from fillpdf import fillpdfs
'''
The Pdf class is used to read pdf form`s field in memory

The json object properties

Name        :   the name of the task
Kind        :   pdf
Description :   the description of the task
Template    :   the PDF used as template
Output      :   the output PDF file
Type        :   the type of the output, can be file or memory
'''
class FillPdf(BaseTask):
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.template = get_dict_value(jsondata,'Template')
        self.output = get_dict_value(jsondata,'Output')
        self.type = get_dict_value(jsondata,'Type')
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

	#def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = position  # not used for now
        _ = mapref # not used for now
        _ = g_rows

        form_fields = list(fillpdfs.get_form_fields(replace_global_parameter(self.template, g_rows)).keys())

        fillpdfs.write_fillable_pdf(replace_global_parameter(self.template, g_rows),replace_global_parameter(self.output, g_rows), None)

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class