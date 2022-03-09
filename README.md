# pyarchive
PYArchive is a tool in python to archive in csv/excel files data from databases. I created the tool because I was fed up to use copy/pase from Microsoft SQL studio to put the information into a Excel file. 
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
The json paramater file has 2 sections

1: Connections: is an array of json objects with the below definition

    Connection object definition
        Name        : the name of the connection that will be used by tasks
        Connection  : the connection string to connect to the database

2: Tasks: is an array of json objects with definitions below


Task's Kinds
    array       :   create a simple list of scalar values in memory. the name of the array is also the name of the column created in memory
    csv         :   read a csv file in memory
    query       :   execute a SQL query or a stored procedure
    save        :   save into a csv/excel file information created by previous tasks
    template    :   save into a excel file information from memory created by previous task with an excel template

Array definition
    Name        :   the name of the task
    Kind        :   array
    Description :   the description of the task
    Command     :   contains the list of values separated by a pipe |

Csv definition
    Name        :   the name of the task
    Kind        :   csv
    Description :   the description of the task
    File        :   the input csv file

Query definition
    Name            :   name of the task
    Kind            :   query
    Description     :   the description of the task
    Connection      :   the connection's name to use for the query from the connection section
    Command         :   the SQL or stored procecure to execute
    Output          :   the output type of the query (memory,reference, csv or excel)
                        ex: select * from employees where name = '{{name}}' and email = '{{email}}'
                        reference:  means that the query is not executed right away, but will be executed when a parameter will use it.
                        memory:     means that the result will be put in memory
                        csv,excel:  means that the result will be saved into a csv or excel file.
    File            :   the destination file name if the output is csv or excel
    Excluded        :   the list of columns to exclude from the output
    Anonymized      :   the list of columns to anonymize
    Parameters      :   a list of parameter's objects used to execute the query

Parameter definition
    Kind    :   memory    :  means that the parameter rows comes from a list in memory
                reference :  means that the parameter rows comes from a source of type 'reference' that contains also parameters
                child     :  means that the parameter rows comes from the previous parameter definition, so this one is a child.
    Source  :   the name of the memory object that contains the rows
    Names   :   the list of parameters' names separated by comma that will be used into the queries ex: ['{{name}}','{{email}}']
    Fields  :   the list of fields from the source that will replace parameters into the queries: ex: ['name','email']

Save definition
    Name        :   the name of the task
    Kind        :   save
    Description :   the description of the task
    Output      :   csv or excel
    Source      :   the name of the source data to save
    File        :   the output file name
    Excluded    :   a list of excluded columns
    Anonymized  :   a list of columns to anonymize

Template definition
    Name        :   the name of the task
    Kind        :   template
    Description :   the description of the task
    File        :   the excel output file
    Template    :   the excel template file to use

Example with a SQL and a Stored procedure with parameters to put into different excel files the MGMT and SUPPORT information from the database

{
    "Connections" : [
        {
            "Name" : "project",
            "Connection" : "Trusted_Connection=yes;DRIVER={SQL Server Native Client 11.0};SERVER=CA-LC6G5KC2\\SQLEXPRESS;DATABASE=psa_tempo_invoice;UID=saa;PWD=aaa"
        }
    ],
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
```

V 0.3 (March 2022)
