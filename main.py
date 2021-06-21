from connection.connection import ConnectionMng
from ajson.archivejson import ArchiveJson
from connection.connection import ConnectionMng
from task.task import Task
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from message.message import gmsg

def set_logging(file):
    print('Starting configuring the logging on file : ' + file)
    try:
        log_format = (
                '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
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
        print('Completed setting the logging with success')
    except Exception as inst:
        print('Error configuring the logging, check the security for file : ' + file)
        print('The file needs read/write access')
        print('Error message : ' + str(inst))
        sys.exit(1)
    #try
#def


def main() :
    set_logging('pyarchive.log')
    logging.info(gmsg.get(56)) #started
    args = sys.argv[1:]
    data = ArchiveJson().load(args[0])
    con = ConnectionMng(data)
    con.validate()
    task = Task(data)
    task.validate(con)
    task.run(con)
    logging.info(gmsg.get(57)) #completed
#def

main()