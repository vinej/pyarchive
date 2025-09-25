from output.memory import Memory
from output.util import get_dict_value, replace_global_parameter
import logging
from message.message import gmsg
from task.base import BaseTask
import sys
from pypdf import PdfReader, PdfWriter
from pypdf import generic as pypdf_generic

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
class Pdf(BaseTask):
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

        reader = PdfReader(replace_global_parameter(self.template, g_rows))
        writer = PdfWriter(clone_from=reader)               # <--- 
        writer.set_need_appearances_writer(True)
        fields = reader.get_fields()

        '''
        field_object.get('/T', '')

        fields = reader.get_fields()
        field_values = {}

        for page_nr, page in enumerate(writer.pages):
            form_fields = page.get('/Annots')
            if form_fields:
                for field in form_fields.get_object():
                    field_object = field.get_object()

                    # any other logic
                    if 'LastName' in field_object.get('/T', ''):
                        field_object[pypdf_generic.NameObject('/V')] = pypdf_generic.create_string_object("jyv")
            
   
        '''
        #for field_name in fields.keys():
        #    keyval = fields[field_name]
        #    if (keyval.field_type is None) :
        #        continue

            #if keyval.field_type == '/Btn':  # Button field (e.g., checkbox, radio button)
            #    field_values[field_name] = 'Yes' if keyval.get('/V') == '/Yes' else 'Off'
        #    if keyval.field_type == '/Tx' and 'LastName'  in field_name and 'Page1[0]' in field_name:  # Text field
        #        field_values[field_name] = 'jyv'
            #$elif keyval.field_type == '/Ch':  # Choice field (e.g., dropdown, listbox)
            #field_values[field_name] = keyval.get('/V', 'jyv')
            #lif keyval.field_type == '/Sig':  # Signature field
            #   field_values[field_name] = keyval.get('/V', 'jyv')  
        #    else:
        #        continue
            
        #for page in reader.pages:
        #    writer.add_page(page)

        #writer.clone_reader_document_root(reader)

        #writer.update_page_form_field_values(writer.pages[0], field_values)
        #fields_to_change = {"Last Name.": "jyv"}


        # Make changes per page
        # <--    change the looping
        data_dict = { 'LastName[0]': 'jyv' }

        try:
            for page in writer.pages:
                annotations = page.get('/Annots')
                if annotations != None:
                    for annotation in annotations:
                        if annotation['/Subtype'] == '/Widget':
                            if annotation['/T']:
                                key = annotation['/T']
                                if key in data_dict.keys():
                                    annotation.update({
                                        pypdf_generic.NameObject("/V"): pypdf_generic.create_string_object(data_dict[key])
                                        #pypdf_generic.NameObject("/Ff"): pypdf_generic.NumberObject(1)  # Set the ReadOnly flag
                                    })


        except Exception as e:
            logging.critical(gmsg.get(3), "Error", e)


        #for page in enumerate(writer.pages):
        #    writer.update_page_form_field_values( page, { 'LastName[0]', 'jyb'}, auto_regenerate=False)


        # <-- simpler
        writer.write(replace_global_parameter(self.output, g_rows))
        #with open(replace_global_parameter(self.output, g_rows), "wb") as f:
        #    writer.write(f)

        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class