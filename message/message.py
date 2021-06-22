class Message:
    def __init__(self):
        self.mapmsg = {}

        self.mapmsg[2] = "Message ID not found into the list"
        self.mapmsg[3] = "Array '%s' completed"
        self.mapmsg[7] = "RUN Error: Error opening log file"
        self.mapmsg[8] = "START processing"
        self.mapmsg[9] = "END processing"

        self.mapmsg[11] = "JSON Connection Error: the connection' name '%s' at the position '%s' already exists"
        self.mapmsg[12] = "JSON Connection Error: the connection at the position '%s' does not contains the field '%s'"

        self.mapmsg[18] = "INFO: Saving into CSV with the query: '%s'"
        self.mapmsg[19] = "FATAL: Failed to open file"
        self.mapmsg[20] = "RUN Error: failed to open file output CSV file '%s'"
        self.mapmsg[21] = "INFO: Success saved into the CSV file '%s'"
        self.mapmsg[22] = "INFO: Starting saving into the CSV file '%s'"
        self.mapmsg[23] = "INFO: Starting saving into the Excel file '%s'"
        self.mapmsg[24] = "INFO: Saving into Excel with the query: '%s'"
        self.mapmsg[25] = "INFO: Success saved into the Excel file '%s'"
        self.mapmsg[26] = "JSON Error: The task at position '%d' does not contains the field '%s'"
        self.mapmsg[27] = "JSON Error: The task at position '%d' with the name '%s' does not contains the field '%s'"
        self.mapmsg[28] = "JSON Error: The task at position '%d' with the name '%s' does not support the OutputType: '%s'"
        self.mapmsg[29] = "JSON Error: The supported OutputType is <memory> only"

        self.mapmsg[30] = "JSON Parameter Error at position %s of the task at position %s: the <Source> reference' name does not exist in other tasks"
        self.mapmsg[31] = "JSON Parameter Error: the task '%s' at position '%s': the first parameter must have a <Kind> equal to '%s'"
        self.mapmsg[32] = "JSON Parameter Error: the parameter at position '%s' of the task at position '%s' does not contains the field <%>"
        self.mapmsg[33] = "JSON Parameter Error at position '%s' of the task at position '%s': the kind '%s' is not supported"
        self.mapmsg[34] = "JSON Parameter Error: The supported kind are '%s' and '%s' only"
        self.mapmsg[35] = "JSON Parameter Error at position '%s' of the task at position '%s': <UseDatabase> is not supported for kind '%s'"

        self.mapmsg[36] = "JSON Query Error at the task position '%s': the connection '%s' does not exist into the connections' section:"
        self.mapmsg[37] = "JSON Query Error: The task at position '%s' does not contains the field '%s'"
        self.mapmsg[38] = "JSON Query Error: The task at position '%s' with the name '%s' does not contains the field '%s'"
        self.mapmsg[30] = "JSON Query Error at the task at position '%s' with the name '%s': the kind '%s' is not supported"
        self.mapmsg[40] = "JSON Query Error: the supported kind are '%s','%s','%s'"
        self.mapmsg[41] = "JSON Query Error: the task at position '%s' with the name '%s' does not suport the OutputType '%s'"
        self.mapmsg[42] = "JSON Query Error: the supported type are '%s','%s','%s','%s'"
        self.mapmsg[43] = "JSON Query Error: the task at position '%s' with the name '%s' the output type '%s' must have a field '%s'"
        self.mapmsg[44] = "JSON Query Error: the first parameter of a query task cannot have the kind <%>"
        self.mapmsg[45] = "JSON Query Error: the source '%s' is not available. Maybe you used a <reference> instead of <memory> OutputType for the task"
        self.mapmsg[46] = "JSON Query Error: the output type '%s' is not supported, check for a typo"
        self.mapmsg[47] = "JSON Task Error at the task position '%d': the task name '%s' already exist"
        self.mapmsg[48] = "JSON Task Error: the task at the position '%s' does not contain the field '%s'"
        self.mapmsg[49] = "JSON Task Error: the task at the position '%s' with the name '%s' does not contain the field '%s'"
        self.mapmsg[50] = "JSON Task Error: the task at the position '%s' with the name '%s' the kind '%s' is not supported"
        self.mapmsg[51] = "JSON Task Error: the supported tasks are '%s','%s','%s'"
        self.mapmsg[52] = "INFO: Columns:%s "
        self.mapmsg[53] = "INFO: Anonymized column '%s' with the value '%s'"
        self.mapmsg[54] = "INFO: Anonymized value for the column '%s' with the value '%s' is '%s'"
        self.mapmsg[55] = "INFO: Waiting for all go routines to complete"
        self.mapmsg[56] = "Pyarchive started"
        self.mapmsg[57] = "Pyarchive comptleted with success"
        self.mapmsg[58] = "The field 'Kind' is missging and it's mandatory"
    #def

    def get(self,id):
        return  self.mapmsg[id]
    #def
#class

gmsg = Message()