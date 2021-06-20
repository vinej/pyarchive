import sys

class Connection:
    def __init__(self,data):
        self.name = data['Name']
        self.connection = data['Connection']
    #def
#class

class ConnectionMng:
    def __init__(self, data):
        mapjsoncon = data['Connections']
        self.mapcon = []
        for c in mapjsoncon:
            self.mapcon.append(Connection(c))
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
    #def
#class

