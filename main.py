from message.message import gmsg
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from connection.connection import ConnectionMng
from ajson.archivejson import ArchiveJson
from connection.connection import ConnectionMng
from task.task import Task

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


def main() :
    set_logging('pyarchive.log')
    try:
        # get started
        logging.info(gmsg.get(56)) #started
        args = sys.argv[1:]
        # read the json file to execute
        jsondata = ArchiveJson().load(args[0])
        # get all connections
        mapcon = ConnectionMng(jsondata)
        # validate the connections
        mapcon.validate()
        # get all tasks to execute
        tasks = Task(jsondata)
        # validate the tasks
        tasks.validate(mapcon)
        # run the tasks
        tasks.run(mapcon)
        # completed
        logging.info(gmsg.get(57)) #completed
    except Exception as e:
        logging.fatal(gmsg.get(1), e)
    #try
#def

main()