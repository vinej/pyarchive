from output.memory import Memory
from output.util import get_dict_value, replace_global_parameter
import logging
from message.message import gmsg
from task.base import BaseTask
import sys
from pypdf import PdfReader, PdfWriter
from pypdf import generic as pypdf_generic
#from pdfrw import PdfReader, PdfDict, PdfName, PdfObject, PdfWriter
from itertools import groupby

'''
The Pdf class is used to read pdf form`s field in memory

The json object properties

Name        :   the name of the task
Kind        :   pdf
Description :   the description of the task
Template    :   the PDF used as template
Output      :   the output PDF file
Type        :   the type of the output, can be file or memory
Dict        :   the dictionary of field to fill in the pdf form
'''
class Pdf(BaseTask):
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.template = get_dict_value(jsondata,'Template')
        self.output = get_dict_value(jsondata,'Output')
        self.type = get_dict_value(jsondata,'Type')
        self.dict = get_dict_value(jsondata,'Dict')
    #def

    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

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

    def split_by_mixcase_groupby(self, text):
        return " ".join(["".join(g) for k, g in groupby(text, key=str.isupper)])
    #def

    def find_annotations_keys(self, pages):

        out_keys = []

        for page in pages:
            annotations = page[self.ANNOT_KEY]
            for annotation in annotations:
                if annotation[self.SUBTYPE_KEY] == self.WIDGET_SUBTYPE_KEY:
                    if annotation[self.ANNOT_FIELD_KEY]:
                        out_keys.append(annotation[self.ANNOT_FIELD_KEY])

        return out_keys
    #def

    def fix_dict(self, outkeys):

        mykeys = self.dict.keys()
        tmp = {}

        for key in mykeys:
            for akey in outkeys:
                if key.lower() in akey.lower():
                    tmp[akey] = self.dict[key]
        
        for key in mykeys:
            skey = self.split_by_mixcase_groupby(key)
            for akey in outkeys:
                if skey.lower() in akey.lower():
                    # do not add exsiting key
                    if skey.lower() != akey.lower():
                        tmp[akey] = self.dict[key]

        self.dict.update(tmp)
    #def

    def run(self, mapmem, mapref, mapcon, position, g_rows):
        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapcon    # not used for now
        _ = position  # not used for now
        _ = mapref # not used for now
        _ = g_rows

        pdfOut = replace_global_parameter(self.output, g_rows)

        merger = PdfWriter()

        reader = PdfReader(replace_global_parameter(self.template, g_rows))
        reader.add_form_topname(self.name)
        writer = PdfWriter(clone_from=reader)

        keys = self.find_annotations_keys(writer.pages)

        self.fix_dict(keys)

        # Update form fields for each page in the current PDF
        for page in writer.pages:
            print("page",page.page_number)
            writer.update_page_form_field_values(
                page,
                self.dict,
                auto_regenerate = False
            )
    
        merger.append(writer)

        # Write the merged PDF to the output file
        merger.write(pdfOut )
        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class