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
            gparam.set_layer_mapmem(5)

            # maximum of 5 layers of GlobalParameters, for each layers, maye it's needed
            # to rerun the the current task before looping on the task records
            for g_row0 in gparam.mapmem[gparam.vtasks[0].name].rows:
                # if the gparam.vtask[0] is of type reference, we must re-run the task as 'memory' because
                # the task could use GlobalParameters that need to be fixed before doing the real call
                if gparam.vtasks[1].output == 'reference' :
                    g_rows =  { gparam.vtasks[0].name: g_row0 }
                    gparam.run_task(mapcon, gparam.vtasks[1], 1, g_rows)
                #if
                for g_row1 in gparam.mapmem[gparam.vtasks[1].name].rows:
                    if gparam.vtasks[2].output == 'reference' :
                        g_rows =  { gparam.vtasks[0].name: g_row0, gparam.vtasks[1].name: g_row1}
                        gparam.run_task(mapcon, gparam.vtasks[2], 2, g_rows)
                    #if
                    for g_row2 in gparam.mapmem[gparam.vtasks[2].name].rows: 
                        # if the gparam.vtask[0] is of type reference, we must re-run the task as 'memory' because
                        # the task could use GlobalParameters that need to be fixed before doing the real call
                        if gparam.vtasks[3].output == 'reference' :
                            g_rows =   { gparam.vtasks[0].name: g_row0, gparam.vtasks[1].name: g_row1, gparam.vtasks[2].name: g_row2}
                            gparam.run_task(mapcon, gparam.vtasks[3], 3, g_rows)
                        #if
                        for g_row3 in gparam.mapmem[gparam.vtasks[3].name].rows: 
                            # if the gparam.vtask[0] is of type reference, we must re-run the task as 'memory' because
                            # the task could use GlobalParameters that need to be fixed before doing the real call
                            if gparam.vtasks[4].output == 'reference' :
                                g_rows =  { gparam.vtasks[0].name: g_row0, gparam.vtasks[1].name: g_row1,
                                            gparam.vtasks[2].name: g_row2, gparam.vtasks[3].name: g_row3 }
                                gparam.run_task(mapcon, gparam.vtasks[4], 4, g_rows)
                            #if
                            for g_row4 in gparam.mapmem[gparam.vtasks[4].name].rows: 
                                g_rows =  { gparam.vtasks[0].name: g_row0, gparam.vtasks[1].name: g_row1,
                                            gparam.vtasks[2].name: g_row2, gparam.vtasks[3].name: g_row3,
                                            gparam.vtasks[4].name: g_row4} 

                                tasks.run(mapcon, g_rows)
                                # recreate the tasks for the next run
                                # free memory
                                tasks = None
                                tasks = Task(jsondata)
                                tasks.validate(mapcon)
                            #for
                        #for
                    #for
                #for
            #for
        else:
            g_row = None
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