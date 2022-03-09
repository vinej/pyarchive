# pyarchive
Archive data tools in python (python 3.9.x)

This small utility could be used to archive data from differents sources (csv,excel,db).
The utility takes a json file in parameter.


The json file has 2 section

1: connections
    This section define connections used by the tasks

2: tasks
    This section define the task that will run sequentialy
    a task can use the information created by previous tasks as parameters

Task's Kinds
    array       :   create a simple list of scalar value in memory
    csv         :   read a csv file in memory
    query       :   execute a SQL/SP query
    save        :   save into a csv/excel file information created by previous tasks
    template    :   save into a Excel file the information from memory with an excel template

Array definition
    Name        :   the name of the task
    Kind        :   array
    Description :   the description of the task
    Command     :   contains the list of values separated by a pipe |
    Output      :   memory

Csv definition
    Name        :   the name of the task
    Kind        :   csv
    Description :   the description of the task
    File        :   the input csv file
    Output      :   memory 

Query definition
    Name            :   name of the task
    Kind            :   query
    Description     :   the description of the task
    Connection      :   the connection name to use for the query
    Command         :   the SQL or stored proc to execute
    Output          :   the output type of the query (memory,csv or excel)
    File            :   the destination file name if the output is csv or excel
    Excluded        :   the list of columns to exclude from the ouput
    Anonymized      :   the list of columns to anonymized
    Parameters      :   a list of parameters object used to execute the query

Parameter definition
    Kind    :   memory    :  means that the parameter comes from a static list in memory
                reference :  means that the parameter comes from a source of type 'reference' that contains also parameters
                child     :  means that the parameter comes from the previous parameter definition, so this one is a child.
    Source  :   the name of the memory object that contains the rows
    Names   :   the list of parameters' names separated by comma that will be used into the queries
    Fields  :   the list of fields from the source that will replace parameters into the queries

Save definition
    Name        :   the name of the task
    Kind        :   save
    Description :   the description of the task
    Output      :   csv or excel
    Source      :   the name of the source data to save
    File        :   contains the file name ouput
    Excluded    :   a list of excluded columns
    Anonymized  :   a list of columns to anonymized

Template definition
    Name        :   the name of the task
    Kind        :   template
    Description :   the description of the task
    File        :   the excel output file
    Template    :   the excel template file to use

Example with a SQL and a Stored procedure
```
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
            "Description":"activity",
            "Output" : "memory"
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



V 0.2
