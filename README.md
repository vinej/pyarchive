# pyarchive
PYArchive is a tool in python to archive in csv/excel files data from databases. I created the tool because I was fed up to use copy/paste from Microsoft SQL studio to put the information into a Excel file. 
```
    local installation
        1- install pip
        2- pip install pyodbc
        3- pip install openpyxl
```

This small utility could be used to archive data from differents sources (csv,excel,db).

The utility takes a json file as parameter.

Note:  main.exe is a window executable created with pyinstaller

```
The json parameter file has 3 sections : Connections, GlobalParameter, Tasks

1: Connections: is an array of connections to the database used by the GlobalParameter and Tasks sections.
        The object definition:  

        Name        : the name of the connection that will be used by tasks
        Connection  : the connection string to connect to the database

        Example
        "Connections" : [
            {
                "Name" : "project",
                "Connection" : "Trusted_Connection=yes;DRIVER={SQL Server Native Client 11.0};SERVER=CA-LC6G5KC2\\SQLEXPRESS;DATABASE=psa_tempo_invoice;UID=saa;PWD=aaa"
            }
        ],....

2: GlobalParameters: This option is used to run all tasks many time from a list of values with a maximum of 5 levels of loop.

        The internal loops are like that

            for row1 in rows level1 
                for row2 in rows level2
                    for row3 in rows level3
                        for row4 in rows level4
                            for row5 in rows level5

                                execute all tasks with global parameters row1,row2,rows3,row4,row5

        Example, you maybe want to run tasks for all databases. For each database, run for all projects into the database. For each project run for each periode of the project. This kind of user case with have 3 levels.

        - the level2, level3,level4,level5 tasks can used also parameters from the previous level. In that case the output type must be 'reference' instead of 'memory'
        - an output type 'reference' means that the task is not executed right away the first time. The task is put in memory to be re-run with parameters updated with
        - values from previous tasks

        the list of values is created from a Task of type array, csv or query
        the parameter variables uses [[name.column]] in the Tasks definition section to access the current row and field of the current iteration (loop)
        by example, this option can be used to run all tasks for project 'prj1' and 'prj2'

        Example to loop on a fixed list of projects
        "GlobalParameters":
        [
            { 
                "Name" : "project",
                "Kind" : "array",  
                "Description" : "read list of projects into memory",
                "Command" : "prj1|prj2"
            }
        ],...
        see the task definition below

3: Tasks: tasks are commands run sequentialy from task definition below. There is 5 kinds of task:
    array       :   create a simple list of scalar values in memory. the name of the array is also the name of the column created in memory
    csv         :   read a csv file in memory. the first line of the CSV must contains the columns' names
    query       :   execute a SQL query or a stored procedure and save the result
    save        :   save into a csv/excel file information created by previous tasks in memory
    curl        :   launch a curl command (not completed yet, on progress)

Array definition
    Name        :   the name of the task
    Kind        :   array
    Description :   the description of the task
    Command     :   contains the list of values separated by a pipe |

Csv definition
    Name        :   the name of the task
    Kind        :   csv
    Description :   the description of the task
    File        :   the full path of the csv file

Query definition
    Name            :   name of the task
    Kind            :   query
    Description     :   the description of the task
    Connection      :   the connection's name to use for the query from the connection section
    Command         :   the SQL or stored procecure to execute
                        ex: select * from employees where name = '{{name}}' and email = '{{email}}'
    Output          :   the output type of the query (memory,reference, csv or excel)
                        reference:  means that the query is not executed right away, but will be executed when a parameter will use it.
                        memory:     means that the result will be put in memory
                        csv,excel:  means that the result will be saved into a csv or excel file.
    File            :   the destination file name if the output is csv or excel
    ExcelTemplate   :   a excel template to use for the output of type Excel (see into Save task for template rules for ExcelTemplate)
    Excluded        :   the list of columns to exclude from the output
    Anonymized      :   the list of columns to anonymize on the output
    Parameters      :   a list of parameter's objects used to execute the query

    Parameter definition
        Kind    :   memory    :  means that the parameter rows comes from a list in memory
                    reference :  means that the parameter rows comes from a source of type 'reference' that contains also parameters
                    child     :  means that the parameter rows comes from the previous parameter definition, so this one is a child.
        Source  :   the name of the memory object that contains the rows
        Names   :   the list of parameters' names separated by comma that will be used into the queries ex: ['{{name}}','{{email}}']
        Fields  :   the list of fields from the source that will replace parameters into the queries: ex: ['name','email']

Save definition
    Name            :   the name of the task
    Kind            :   save
    Description     :   the description of the task
    Output          :   csv or excel
    Source          :   the name of the source data to save
    File            :   the output file name
    Excluded        :   a list of excluded columns
    Anonymized      :   a list of columns to anonymize
    ExcelTemplate   :   a excel template to use for the output of type Excel

        Excel template rules
            - the excel template can have many tabs
            --> the title of each tab is the memory source name to use for dynamic rows
            - the dynamic region of each tab is define between [[begin]] and [[end]]
            - the dynamic section could have one to many lines
            - into the dynamic section, the fields with {{...}} will be replaced with the information from the source rows
            - the template support styles and formulas

            Excel template
                A               B               C                    D
            1  First Name       Last Name       Full Name           Occupation
            2  [[begin]]			
            3  {{first_name}}   {{last_name}}   =A3&","&B3          {{occupation}}	                                                     	
            4  [[end]]
            
            result
                A                  B               C                  D
            1  First Name       Last Name       Full Name           Occupation
            2  John             Doe             John,Doe            gardener
            3  Lucy             Smith           Lucy,Smith          teacher
            4  Brian            Bethamy         Brian,Bethamy       programmer


Curl definition  (see curl documentatuion 7.82 on Internet)
    Name:               name of the task
    Kind:               curl
    Description:        description of the task
    Output:             memory or reference
    Options:            an array of curl option' objects (see curl documentation version 7.82)
                        see below example. You can have one to many options.
                        the first one is often the URL of the call supported by curl
    Parser:             the parser to use to decode the result (html,text,css,csv,json,xml)

                        NOTE: into the curl options, " must be escape for \"
                        NOTE: for html,text,css, only one colum, is created with the name of the task's name

        { 
            "Name" : "google",
            "Kind" : "curl",  
            "Description":"get the google html page",
            "Output" : "memory",
            "Options" : [
                { "Option": 'http://www.google.com' }
            ],
            "Parser": "html"
        },
        { 
            "Name" : "json",
            "Kind" : "curl",  
            "Description":"get a json file",
            "Output" : "memory",
            "Options" : [
                { "Option": "file://c:/curl/test_json.json"},
                { "Option": "-H \"X-Custom-Header: value\"" },
                { "Option": "-H \"Content-Type: application/json\"" }             
            ],
            "Parser" : "json"
        },
        { 
            "Name" : "xml",
            "Kind" : "curl",  
            "Description":"get a xml file",
            "Output" : "memory",
            "Options" : [
                { "Option": "file://c:/curl/test_xml.xml"},
                { "Option": "-H \"X-Custom-Header: value\"" },
                { "Option": "-H \"Content-Type: application/xml\"" }             
            ],
            "Parser" : "xml"
        }

========
Examples
========

Example of a json file to use with pyarchive
{
    "Connections" : [
        {
            "Name" : "project",
            "Connection" : "Trusted_Connection=yes;DRIVER={SQL Server Native Client 11.0};SERVER=CA-LC6G5KC2\\SQLEXPRESS;DATABASE=psa_tempo_invoice;UID=saa;PWD=aaa"
        }
    ],
    "GlobalParameters": [],
    "Tasks" : [
        { 
            "Name" : "activity",
            "Kind" : "array",  
            "Command":"MGMT|SUPPORT",
            "Description":"activity"
        }
        ,
        { 
            "Name" : "tempo",
            "Kind" : "query",  
            "Description" : "tempo",
            "Connection" : "project",
            "Command":"select * from dbo.tempo where activity='{act}'",
            "Output" : "excel",
            "File" : "tempo.xlsx",
            "Parameters" : [
                {
                    "Names" : ["{act}"],
                    "Kind": "memory",
                    "Fields" : ["activity"],
                    "Source": "activity"
            }]
        }
        ,
        { 
            "Name" : "tempo2",
            "Kind" : "query",  
            "Description" : "tempo",
            "Connection" : "project",
            "Command":"exec dbo.test '{act}'",
            "Output" : "excel",
            "File" : "tempo2.xlsx",
            "Parameters" : [
                {
                    "Names" : ["{act}"],
                    "Kind": "memory",
                    "Fields" : ["activity"],
                    "Source": "activity"
            }]
        }
    ]
}

an example with GlobalParameter and ExcelTemplate
{
    "Connections" : [],
    "GlobalParameters":
    [
        { 
            "Name" : "project",
            "Kind" : "array",  
            "Description" : "read list of projects into memory",
            "Command" : "prj1|prj2"
        }
    ]
    ,
    "Tasks" : [
        { 
            "Name" : "users",
            "Kind" : "csv",  
            "Description" : "read list of users into memory",
            "File" : "users_[[project.project]].csv"
        },
        {
            "Name"          :   "template",
            "Kind"          :   "save",  
            "Source"        :   "users",
            "Description"   :   "test template2",
            "File"          :   "C:/Users/jyvin/OneDrive/Documents/GitHub/pyarchive/out_[[project.project]]_template2.xlsx",
            "ExcelTemplate" :   "C:/Users/jyvin/OneDrive/Documents/GitHub/pyarchive/template2.xlsx"
        }
    ]
    }
```
V 0.4 (March 2022)
