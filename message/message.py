class Message:
    def __init__(self):
        self.mapmsg = {}
        self.mapmsg[1] = "RUN: Runtime unexpected exception: '%s'"
        self.mapmsg[2] = "Configuration of the logging into file '%s' is starting"
        self.mapmsg[3] = "RUN: Task of kind '%s' with name '%s' is completed"
        self.mapmsg[4] = "RUN: Task of kind '%s' with name '%s' is starting"
        self.mapmsg[5] = "Configuration of the logging into file '%s' is completed"
        self.mapmsg[6] = "Error configuring the logging, check the security for file '%s'"
        self.mapmsg[7] = "The file '%s' needs read/write access"
        self.mapmsg[11] = "JSON: The connection' name '%s' at the position '%s' already exists"
        self.mapmsg[12] = "JSON: The connection at the position '%s' does not contains the field '%s'"

        self.mapmsg[26] = "JSON: The task at position '%s' does not contains the field '%s'"
        self.mapmsg[27] = "JSON: The task at position '%s' with the name '%s' does not contains the field '%s'"
        self.mapmsg[28] = "JSON: The task at position '%s' with the name '%s' does not support the OutputType: '%s'"
        self.mapmsg[29] = "JSON: The supported OutputType is <memory> only"
        self.mapmsg[32] = "JSON: the parameter at position '%s' of the task at position '%s' does not contains the field <%>"

        self.mapmsg[56] = "Pyarchive started"
        self.mapmsg[57] = "Pyarchive comptleted with success"
    #def

    def get(self,id):
        return  self.mapmsg[id]
    #def
#class

gmsg = Message()