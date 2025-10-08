import logging
from message.message import gmsg
from output.util import get_dict_value

'''
Connection class

Parameter: json object of type connection
'''
class Connection:
    def __init__(self,jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.connection = get_dict_value(jsondata,'Connection')
    #def
#class

'''
Class to manage all connections for the tasks

Parameter: a json data object

'''
class ConnectionMng:
    def __init__(self, jsondata):
        # get the connections section of the json object
        mapjsoncon = jsondata['Connections']
        self.mapcon = []
        position = 1
        # create a map of all connections
        for c in mapjsoncon:
            self.mapcon.append(Connection(c))
            position = position + 1
        #for
    #def

    def get_mapcon(self):
        return self.mapcon
    #def

    # get a connection by name
    def get_con(self, name):
        for c in self.mapcon:
            if name == c.name:
                return c
            #if
        #for
        return None
    #def

    # validate all connections
    def validate(self): 
        position = 1
        for con in self.mapcon:
            self.validate_con(con, position)
            position = position + 1
        #for
    #def 

    # validate a connection at position x
    def validate_con(self, con, position):  
        if con.name == None:
            logging.fatal(gmsg.get(12), position, 'Name')
        else:
            con.name = con.name.lower()
        #if

        if con.connection == None:
            logging.fatal(gmsg.get(12), position, 'Connection')
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

