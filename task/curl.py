import shlex
import subprocess
from task.memory import Memory
from task.util import get_dict_value
from task.util import replace_global_parameter
from task.util import read_csv
from task.util import read_json
from task.util import read_xml

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
Parser:             one of html,css,text,json,csv,xml
        { 
            "Name" : "google",
            "Kind" : "curl",  
            "Description":"get the google html page",
            "Output" : "memory",
            "Options" : [
                { "Option": 'http://www.google.com' }
            ],
            "Parser" : "html"
        }

        example of curl command : https://reqbin.com/req/c-1n4ljxb9/curl-get-request-example

        get a json file
        { 
            "Name" : "json",
            "Kind" : "curl",  
            "Description":"get the google html page",
            "Output" : "memory",
            "Options" : [
                { "Option": "https://reqbin.com/echo/get/json" },
                { "Option": "-H \"X-Custom-Header: value\"" },
                { "Option": "-H \"Content-Type: application/json\"" },               
            ],
            "Parser" : "json"
        }
'''
class Curl:
    def __init__(self, jsondata):
        self.name =  get_dict_value(jsondata,'Name')
        self.kind =  get_dict_value(jsondata,'Kind')
        self.description =  get_dict_value(jsondata,'Description')
        self.options =  get_dict_value(jsondata, 'Options')
        self.output =  get_dict_value(jsondata, 'Output')
        self.parser = get_dict_value(jsondata, 'Parser')
        self.hierarchy = get_dict_value(jsondata, 'HierarchyProperty')
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


        if self.parser == None or self.parser == 'html' or self.parser == 'css' or self.parser == 'text':
            mapmem[self.name] = stdout
        elif self.parser == 'csv':
            columns, rows = read_csv(stdout)
            mapmem[self.name] = Memory(columns, rows)
        elif self.parser == 'json':
            columns, rows = read_json(stdout)
            mapmem[self.name] = Memory(columns, rows)
        elif self.parser == 'xml':
            columns, rows = read_xml(stdout)
            mapmem[self.name] = Memory(columns, rows)
        else:
            raise Exception("Curl error, parser not implemented: " + self.parser)
        #if
#class

