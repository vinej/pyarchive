from task.util import get_dict_value
import logging
from message.message import gmsg
from output.output import Output
import sys

class Save:
    def __init__(self, data):
        self.name = get_dict_value(data,'Name')
        self.kind = get_dict_value(data,'Kind')
        self.description = get_dict_value(data,'Description')
        self.output = get_dict_value(data,"Output")
        self.file = get_dict_value(data,"File")
        self.source = get_dict_value(data,"Source")
        self.excluded = get_dict_value(data,"Excluded")
        self.anonymized = get_dict_value(data,"Anonymized")
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

        if self.output != 'excel':
            logging.errro(gmsg.get(28), position, self.name, 'Output')
            logging.fatal(gmsg.get(29))
            sys.exit(28)

        #if
	#def

    def run(self, mapmem, mapref, con, position):
        _ = con    # not used for now
        _ = position  # not used for now
        _ = mapref # not used for now
        logging.info(gmsg.get(4), self.kind, self.name)
        m = mapmem[self.source]
        if m != None:
            Output().save(m, self.file, self.name, self.excluded, self.anonymized, self.output)
        #if
        logging.info(gmsg.get(3), self.kind, self.name)
    #def
#class

