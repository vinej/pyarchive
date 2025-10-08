from datetime import datetime
import traceback
import numpy as np
from pandas import DataFrame
import os
import email, smtplib
import logging
from logging.handlers import TimedRotatingFileHandler
import sys, getopt
import zipfile
import win32com.client as win32
import configparser
import openpyxl
import os.path
from os import path, read
import pyodbc


# ini file
# the file psa_tempo_diff.ini must be into the current directory
# with the python program
INI_FILE_NAME = './init.ini'
LOG_NAME = 'init.log'

conProject = None

class inifile:
    def __init__(self,
                 excel_output,
                 corpo_conn_string,
                 project_conn_string,
                 project_query,
                 period_query,
                 report_query,
                 database_query,
                 log_level):
        self.excel_output = excel_output
        self.corpo_conn_string = corpo_conn_string
        self.project_conn_string = project_conn_string
        self.project_query = project_query
        self.period_query = period_query
        self.report_query = report_query
        self.database_query = database_query
        self.log_level = log_level
    #def
#class

class project :
    def __init__(self, pmp_proj, pmp_proj_no, pmp_proj_sourc_no, pmp_db_servr_nm, pmp_db_nm):
        self.pmp_proj = pmp_proj
        self.pmp_proj_no = pmp_proj_no
        self.pmp_proj_sourc_no = pmp_proj_sourc_no
        self.pmp_db_servr_nmm = pmp_db_servr_nm
        self.pmp_db_nm = pmp_db_nm
    #def
#class

class period:
    def __init__(self, period):
        self.period = period
    #def
#class

def error(inst):
    """Process error into console/log """
    logging.error('Error message is : ' + str(inst))
    traceback.print_exception(*sys.exc_info())
#def

def get_logging_level(logging_string):
    if logging_string == "DEBUG":
        return logging.DEBUG
    elif logging_string == "INFO":
        return logging.INFO
    elif logging_string == "WARNING":
        return logging.WARNING
    elif logging_string == "ERROR":
        return logging.ERROR
    elif logging_string == "CRITICAL":
        return logging.CRITICAL
    else:
        return logging.INFO
    #if
#def

def set_logging(oinifile):
    print('Starting configuring the logging on file : ' + LOG_NAME)
    try:
        log_format = (
                '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
        rhandler = TimedRotatingFileHandler(    LOG_NAME,
                                                when="w0",
                                                interval=1,
                                                backupCount=20)
        logging.basicConfig(
            level=oinifile.log_level,
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                rhandler
            ]
        )
        print('Completed setting the logging with success')
    except Exception as inst:
        print('Error configuring the logging, check the security for file : ' + log_file)
        print('The file needs read/write access')
        print('Error message : ' + str(inst))
        sys.exit(1)
    #try
#def

def close_logging():
    logger = logging.getLogger("")
    x = list(logger.handlers)
    for i in x:
        logger.removeHandler(i)
        i.flush()
    i.close()
    #for
#def
    
def load_parameter(argv):
    print('Starting reading the parameter')
    try:
        opts, args = getopt.getopt(argv,"ini")
    except getopt.GetoptError:
        print('Error reading the parameter, use the example below')
        print('Syntax : init.py -ini init.ini')
        sys.exit(2)
    #try
    for opt, arg in opts:
        if opt == '-ini':
            INI_FILE_NAME = arg
        #if
    #for
    print('Completed reading the parameter with success')
#def

def load_ini_file():
    try:
        if os.path.isfile(INI_FILE_NAME):
            print('Starting reading the ini file : ' + INI_FILE_NAME)
            config = configparser.ConfigParser()
            config.read(INI_FILE_NAME)
            ini = inifile(
                config["report"]["excel_output"],
                config["report"]["corpo_conn_string"],
                config["report"]["project_conn_string"],
                config["report"]["project_query"],
                config["report"]["period_query"],
                config["report"]["report_query"],
                config["report"]["database_query"],
                get_logging_level(config["report"]["log_level"])
            )
            print('Completed reading the ini file with success')
            print(ini.report_query)
            return ini
        else:
            print('Error the ini file does not exist : ' + INI_FILE_NAME)
            sys.exit(3)            
        #if
    except Exception as inst:
        print('Error reading the ini file : ' + INI_FILE_NAME)
        error(inst)
        sys.exit(3)
    #try
#def

def read_project_list(oinifile, database):
    con = None
    try:
        logging.info('Starting connecting to database: '+ oinifile.corpo_conn_string)
        con = pyodbc.connect(oinifile.corpo_conn_string)
        cursor = con.cursor()
        try:
            query = oinifile.project_query.replace("{database}", database)
            cursor.execute(query)
            list = []
            row = cursor.fetchone()
            while row:
                list.append(  
                    project( 
                        row[0],row[1],row[2],row[3],row[4]
                    )
                )
                row = cursor.fetchone()
            #while
            logging.info('Completed read_project_list with success')
            #logging.info(list)
            return list
        except pyodbc.DatabaseError as err:
            logging.error(' Error running read_project_list')
            logging.error(str(err))
        finally:
            con.autocommit = True
            con.close()
        #try
    except Exception as e:
        print(str(e))
        if con != None:
            con.close()
        #if
        logging.error(' Error running read_project_list')
        logging.error(str(e))
    #try
#def

def connect_project(oinifile, database):
    con = None
    project_conn_string = oinifile.project_conn_string.replace("{database}", database)
    try:
        logging.info('Project: Starting connecting to database: '+ project_conn_string)
        con = pyodbc.connect(project_conn_string)
        return con
    except pyodbc.DatabaseError as err:
        logging.error(' Error running read_project_list')
        logging.error(str(err))
    #try
#def
    
def read_project_period(oinifile, con, project_id):
    try:
        cursor = con.cursor()
        period_query = oinifile.period_query.replace("{project}", str(project_id))
        cursor.execute(period_query)
        list = []
        row = cursor.fetchone()
        while row:
            list.append(  period( row[0] ))
            row = cursor.fetchone()
        #while
        logging.info('Completed read_project_period with success')
        return list
    except Exception as e:
        print(str(e))
        logging.error(' Error running read_project_period')
        logging.error(str(e))
        return []
    #try
#def
    
def read_report_query(oinifile, con, project_id, period_prev, period_curr):
    try:
        logging.info('Project: Starting read_report_query')
        cursor = con.cursor()
        report_query = oinifile.report_query.replace("{project}", str(project_id))
        #report_query = report_query.replace("{database}", database)
        report_query = report_query.replace("{period_prev}", str(period_prev))
        report_query = report_query.replace("{period_curr}", str(period_curr))
        cursor.execute(report_query)
        #read column header
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        #for
        df = DataFrame(results)
        logging.info('Completed read_report_query with success')
        return df
    except Exception as e:
        print(str(e))
        logging.error(' Error running read_report_query')
        logging.error(str(e))
        
        sys.exit(14)

    #try
#def

def save_to_excel(oinifile, df, project_id, period_prev, period_curr):
    output = oinifile.excel_output
    output = output.replace("{project}", str(project_id))
    output = output.replace("{period_prev}", str(period_prev))
    output = output.replace("{period_curr}", str(period_curr))
    df.to_excel(output)
#def
        
def print_projects(list):
    for p in list:
        print(p.pmp_proj_no)
    #for
#def


def get_database_list() :
    try:
        cursor = con.cursor()
        cursor.execute(oinifile.database_query)
        list = []
        row = cursor.fetchone()
        while row:
            list.append( row[0] )
            row = cursor.fetchone()
        #while
        logging.info('Completed read_database_list with success')
        return list
        sys.exit(14)
    except Exception as e:
        print(str(e))
        logging.error(' Error running read_project_period')
        logging.error(str(e))
        return []
    #try
#def
                   
def doit(oinifile):
    prev_database = None
    con = None
    try:
        logging.info('START')
        for database in get_database_list():
            logging.info('Starding database:' + database)
            projects = read_project_list(oinifile, database)
            for project in projects:
                if project.pmp_proj != -1 and str(project.pmp_proj_sourc_no) == '21':
                    if prev_database != project.pmp_db_nm:
                        if prev_database != None:
                            con.close()
                        #if
                        prev_database = project.pmp_db_nm
                        con = connect_project(oinifile, project.pmp_db_nm)
                    #if
                    logging.info('Starting project:' + str(project.pmp_proj_sourc_no))
                    periods = read_project_period(oinifile, con, project.pmp_proj_sourc_no)
                    if len(periods) > 1:
                        period_prev = periods[0]
                        for period in periods[1:]:
                            period_curr = period
                            df = read_report_query(oinifile, con, project.pmp_proj_sourc_no, period_prev.period, period_curr.period)
                            save_to_excel(oinifile, df, project.pmp_proj_sourc_no, period_prev.period, period_curr.period)
                            #sys.exit(14)
                            period_prev = period_curr
                        #for
                    #if
                #if
            #for
        #for
        logging.info('END')
    except Exception as inst:
        print('Error running the program')
        print('Error message : ' + str(inst))
        logging.error('Error running the program ')
        error(inst)
        sys.exit(14)
    #try
        
#def

if __name__ == "__main__":
    oinifile = None
    try:
        # try to configure the program first
        load_parameter(sys.argv[1:])
        oinifile = load_ini_file()
        set_logging(oinifile)
        print('START processing')
    except Exception as inst:
        print('Unable to configure the program, probably a security issue on the folder/files')
        print('default internal ini file')
        print('Error message : ' + str(inst))
        error(inst)
        sys.exit(15)
    #
    doit(oinifile)
    close_logging()
    print('END processing')
    sys.exit(0)
#if

    



