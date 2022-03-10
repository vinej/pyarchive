from message.message import gmsg
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from connection.connection import ConnectionMng
from ajson.archivejson import ArchiveJson
from connection.connection import ConnectionMng
from task.task import Task
from task.globalparameter import GlobalParameter
import traceback

def set_logging(file):
    print(gmsg.get(2) % file)
    try:
        log_format = (
                '[%(asctime)s] %(levelname)-8s %(name)-12s %(module)s:%(lineno)s %(funcName)s %(message)s')
        rhandler = TimedRotatingFileHandler(    file,
                                                when="w0",
                                                interval=1,
                                                backupCount=20)
        logging.basicConfig(
            level="INFO",
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                rhandler
            ]
        )
        logging.info(gmsg.get(5), file)
    except Exception as e:
        print(gmsg.get(6), file)
        print(gmsg.get(7), file)
        print(gmsg.get(1), e)
    #try
#def

def validate_args(args):
    pass
    if len(args) < 1 or len(args) > 2:
        raise Exception("Invalidid parameters")
    #if
#def



def main() :
    set_logging('pyarchive.log')
    try:
        # get started
        logging.info(gmsg.get(56)) #started
        
        args = sys.argv[1:]

        validate_args(args)
        # read the json file to execute
        jsondata = ArchiveJson().load(args[0])

        # get all connections
        mapcon = ConnectionMng(jsondata)
        # validate the connections
        mapcon.validate()
        # get all loops to execute the tasks
        gparam = GlobalParameter(jsondata)
        gparam.validate(mapcon)
        # get all tasks to execute
        tasks = Task(jsondata)
        # validate the tasks
        tasks.validate(mapcon)
        # run the tasks
        if len(gparam.maptask) > 0:
            gparam.run(mapcon)
            for mem in gparam.mapmem:
                for g_row in gparam.mapmem[mem].rows:
                    tasks.run(mapcon, g_row)
                    # recreate the tasks for the next run
                    # free memory
                    tasks = None
                    tasks = Task(jsondata)
                    tasks.validate(mapcon)
            #for
        else:
            tasks.run(mapcon, g_row)
        #if
        # completed
        logging.info(gmsg.get(57)) #completed
    except Exception as e:
        traceback.print_exception(*sys.exc_info())
        logging.fatal(gmsg.get(1), e)
    #try
#def

main()