import sys
import logging
from message.message import gmsg
from task.util import get_dict_value

class Connection:
    def __init__(self,data):
        self.name = get_dict_value(data,'Name')
        self.connection = get_dict_value(data,'Connection')
    #def
#class

class ConnectionMng:
    def __init__(self, data):
        mapjsoncon = data['Connections']
        self.mapcon = []
        position = 1
        for c in mapjsoncon:
            newcon = Connection(c)
            self.mapcon.append(Connection(c))
            position = position + 1
        #for
    #def

    def get_mapcon(self):
        return self.mapcon
    #def

    def get_con(self, name):
        for c in self.mapcon:
            if name == c.name:
                return c
            #if
        #for
        return None
    #def

    def validate(self): 
        position = 1
        for con in self.mapcon:
            self.validate_con(con, position)
            position = position + 1
        #for
    #def 

    def validate_con(self, con, position):  
        if con.name == None:
            logging.fatal(gmsg.get(12), position, 'Name')
        else:
            con.name = con.name.lower()
        #if

        if con.connection == None:
            logging.fatal(gmsg.get(12), position, 'Connection')
        else:
            con.connection = con.connection.lower()
        #if

        # validate duplicate names
        max = 1
        for c in self.mapcon:
            if max < position:
                if c.name == con.name:
                    logging.fatal(gmsg.get(11), c.name, max)
                #if
                max = max + 1
            #if
        #for
	#def
#class

