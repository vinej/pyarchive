from output.util import get_dict_value
from output.util import replace_global_parameter
import logging
from message.message import gmsg
import sys
import csv
from ldap3 import Server, Connection, ALL, NTLM

from task.base import BaseTask

'''
The ad class is used to read csv file into memory

The json object properties

Name          :   the name of the task
Kind          :   csv
Description   :   the description of the task
Source  :   the source folder for the copy
Destination : the destination folder for the copy
'''

class Ad(BaseTask):
    def __init__(self, jsondata):
        self.name =  get_dict_value(jsondata,'Name')
        self.kind =  get_dict_value(jsondata,'Kind')
        self.description =  get_dict_value(jsondata,'Description')
        self.source =  get_dict_value(jsondata, 'Source')
        self.destination =  get_dict_value(jsondata, 'Destination')
        self.isurl = get_dict_value(jsondata,'IsUrl')

        self.AD_SERVER = 'WUSD033D002MP.wsatkins.com'  # e.g., 'dc01.company.local'
        self.AD_USER = 'wsatkins\\vinej'  # e.g., 'COMPANY\\jdoe'
        self.AD_PASSWORD = '...'
        self.SEARCH_BASE = 'DC=wsatkins,DC=com'  # Adjust to your AD structure

        self.AD_SERVER2 = 'SLI5030.sli.bz'  # e.g., 'dc01.company.local'
        self.AD_USER2 = 'sli\\vinej'  # e.g., 'COMPANY\\jdoe'
        self.AD_PASSWORD2 = '...'
        self.SEARCH_BASE2 = 'DC=sli,DC=bz'  # Adjust to your AD structure

        self.server = None
        self.conn = None

        self.server2 = None
        self.conn2 = None

        self.accounts = {}
        self.firstnames = {}
        self.lastnames = {}
    #def

    # run the Csv task
    def run(self, mapmem, mapref, mapcon, position, g_rows):
        # replace the global parameter

        self.source = replace_global_parameter(self.source, g_rows)
        self.destination = replace_global_parameter(self.destination, g_rows)

        logging.info(gmsg.get(4), self.kind, self.name)
        _ = mapmem
        _ = mapcon    # not used for now
        _ = position  # not used for now
        _ = mapref   # not used for now

        self.enrich_csv(self.source, self.destination)

        logging.info(gmsg.get(3), self.kind,  self.name)
    #def

    
    def remove_domain(self, ad_string):
        # Split on backslash and return the username part
        if '\\' in ad_string:
            return ad_string.split('\\')[1]
        else:
            return ad_string  # Return as-is if no
    #def

    def get_user_info(self,ad_account):
        only_account = self.remove_domain(ad_account)

        if 'sli\\' in ad_account.lower() :
            conn = self.get_connection("sli")
            conn.search(
                search_base=self.SEARCH_BASE2,
                search_filter=f'(sAMAccountName={only_account})',
                attributes=['givenName', 'sn' ]
            )
        else:
            conn = self.get_connection("wsatkins")
            conn.search(
                search_base=self.SEARCH_BASE,
                search_filter=f'(sAMAccountName={only_account})',
                attributes=['givenName', 'sn']
            )

        if conn.entries:
            entry = conn.entries[0]
            first_name = entry.givenName.value if entry.givenName else ''
            last_name = entry.sn.value if entry.sn else ''
            return first_name, last_name
        else:
            return '', ''
    #def

    def get_connection(self, domain) :
        if domain == 'sli' :
            if self.server2 is None: 
                self.server2 = Server(self.AD_SERVER2, get_info=ALL)
                self.conn2 = Connection(self.server2, user=self.AD_USER2, password=self.AD_PASSWORD2, authentication=NTLM, auto_bind=True)
            #if
            return self.conn2
        else:
            if self.server is None:
                self.server = Server(self.AD_SERVER, get_info=ALL)
                self.conn = Connection(self.server, user=self.AD_USER, password=self.AD_PASSWORD, authentication=NTLM, auto_bind=True)
            #if
            return self.conn
        #if
    #def


    #def

    def enrich_csv(self, input_csv, output_csv):
        with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
             open(output_csv, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)
            fieldnames = ['date', 'user', 'first_name', 'last_name']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if self.isurl == 'y' :
                    user = row['user']
                    date = row['date']
                    url = row['url']

                    if user in self.accounts:
                        first_name = self.firstnames[user]
                        last_name = self.lastnames[user]
                    else:
                        first_name, last_name = self.get_user_info(user)
                        self.firstnames[user] = first_name
                        self.lastnames[user] = last_name
                        self.accounts[user] = 'y'
                    #if

                    logging.info(gmsg.get(3), "AD",  self.remove_domain(user))

                    writer.writerow({
                        'date': date,
                        'user': user,
                        'first_name': first_name,
                        'last_name': last_name,
                        'url' : url
                    })
                else :
                    user = row['user']
                    date = row['date']

                    if user in self.accounts:
                        first_name = self.firstnames[user]
                        last_name = self.lastnames[user]
                    else:
                        first_name, last_name = self.get_user_info(user)
                        self.firstnames[user] = first_name
                        self.lastnames[user] = last_name
                        self.accounts[user] = 'y'
                    #if

                    logging.info(gmsg.get(3), "AD",  self.remove_domain(user))

                    writer.writerow({
                        'date': date,
                        'user': user,
                        'first_name': first_name,
                        'last_name': last_name
                    })
            
    #def

    # validate the Csv task
    def validate(self, mapcon, position):  
        _ = mapcon # not use here
        if self.name == None:
            logging.fatal(gmsg.get(26), position, 'Name')
            sys.exit(26)
        #if
        self.name = self.name.lower()

        if self.kind == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Kind')
            sys.exit(27)
        #
        self.kind = self.kind.lower()

        if self.source == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Source')
            sys.exit(27)
        #if

        if self.destination == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Destination')
            sys.exit(27)
        #if
	#def
#class
