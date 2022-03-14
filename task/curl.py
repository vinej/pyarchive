import shlex
import subprocess
from task.memory import Memory
from task.util import get_dict_value
from task.util import replace_global_parameter
from message.message import gmsg
import logging
'''
Name:               name of the task
Kind:               curl
Description:        description of the task
Output:             memory or reference
Options:            an array of curl option object (see curl documentation version 7.82)
                    see below example. UYou can have one to ma many opttions.
                    the first one is often the URL of the call supported by curl
        { 
            "Name" : "google",
            "Kind" : "curl",  
            "Description":"get the google html page",
            "Output" : "memory",
            "Options" : [
                { "Option": 'http://www.google.com' }
            ]
        }
'''
class Curl:
    def __init__(self, jsondata):
        self.name =  get_dict_value(jsondata,'Name')
        self.kind =  get_dict_value(jsondata,'Kind')
        self.description =  get_dict_value(jsondata,'Description')
        self.options =  get_dict_value(jsondata, 'Options')
        self.output =  get_dict_value(jsondata, 'Output')
    #def

    '''
        validate the tasks information before running
    '''
    def validate(self, mapcon, position):
        pass
    #def

    def check_error(self, returncode, stderr, cmd):
        print(returncode)
        if returncode != 0:
            if returncode == 'XX':
                code = 599
            else:
                code = 500 + returncode
            #if
            logging.fatal("Curl error: \r\n"+ gmsg.get(code)+" cmd: \r\n"+cmd)
            raise Exception("Curl error")
        #if
    #def

    # run the Csv task
    def run(self, mapmem, mapref, mapcon, position, g_row):
        #for o in self.options:
        #    o.option = replace_global_parameter(o.option, g_row) + "b"
        #print(self.options)
        out = []
        for opt in self.options:
            value = get_dict_value(opt, "Option")
            value = replace_global_parameter(value, g_row)
            out.append(value)
        #for

        cmd = "curl "+" ".join(out)
        print(cmd)
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.check_error(process.returncode, stderr, cmd)

        mapmem[self.name] = stdout
#class

