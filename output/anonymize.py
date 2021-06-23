class Anonymized:
    def __init__(self):
        self.anodict = {}
        self.anocount = {}
    #def

    def anonymized(self, name, column, value):
        full_name = name + '|||' + column
        if not full_name in self.anodict:
            self.anodict[full_name] = {}
        #if
        full_dict = self.anodict[full_name]
        if not value in full_dict:
            if not full_name in self.anocount:
                self.anocount[full_name] = 0
            #if
            self.anocount[full_name] = self.anocount[full_name] + 1
            full_dict[value] = "{name}_{count}".format(name=column, count=self.anocount[full_name])
        #if
        return full_dict[value]
    #def
#class
ano = Anonymized()
