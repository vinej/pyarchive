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
The json paramater file has 3 sections : Connections, GlobalParameter, Tasks

1: Connections: is an array of json objects with the below definition to connect to databases

    Connection object definition
        Name        : the name of the connection that will be used by tasks
        Connection  : the connection string to connect to the database

2: GlobalParameter: Is an object that include a Task that will be used to run all tasks for all occurence in memory
        only array,csv,query tasks are available in the section GlobalParameter
        the parameter variables uses [[xxx]] in the tasks definition to access the current row and field of the current iteration (loop)
        by example, this option can be used to run all tasks for all projects

3: Tasks: is an array of json objects with definitions below

Task's Kinds available
    array       :   create a simple list of scalar values in memory. the name of the array is also the name of the column created in memory
    csv         :   read a csv file in memory. the first line of the CSv must contains the columns' names
    query       :   execute a SQL query or a stored procedure and save the result
    save        :   save into a csv/excel file information created by previous tasks in memory
    template    :   save into a excel file information created by previous tasks in memory with the help of an excel template

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
    File        :   the full path of the excel output file
    Template    :   the full path of excel template file to use

    Excel template rules
        - the excel template can have many tabs
        --> the title of each tab is the memory source name to use for dynamic rows
        - the dynamic region of each tab is define between [[begin]] and [[end]]
        - the dynamic section could have one to many lines
        - into the dynamic section, the fields with {{...}} will be replaced with the information from the source rows
        - the template support styles and formulas

        Excel template
               A               B               C                    D
        1  first_name       last_name       full_name           occupation
        2  [[begin]]			
        3  {{first_name}}   {{last_name}}   =A3&","&B3          {{occupation}}	                                                     	
        4  [[end]]
		
        result
             A                  B               C                  D
        1  first_namw       last_name       full_name           occupation
        2  John             Doe             John,Doe            gardener
        3  Lucy	            Smith           Lucy,Smith          teacher
        4  Brian            Bethamy         Brian,Bethamy       programmer


Example of a json file to use with pyarchive

{
    "Connections" : [
        {
            "Name" : "project",
            "Connection" : "Trusted_Connection=yes;DRIVER={SQL Server Native Client 11.0};SERVER=CA-LC6G5KC2\\SQLEXPRESS;DATABASE=psa_tempo_invoice;UID=saa;PWD=aaa"
        }
    ],
    "GlobalParameter": [],
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

an example with GlobalParameter
{
    "Connections" : [],
    "GlobalParameter":
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
            "Name" : "csv1",
            "Kind" : "csv",  
            "Description" : "read list of users into memory",
            "File" : "users_[[project]].csv"
        },
        {
            "Name" : "template2",
            "Kind" : "template",  
            "Description" : "test template2",
            "File":"C:/Users/jyvin/OneDrive/Documents/GitHub/pyarchive/out_[[project]]_template2.xlsx",
            "Template" : "C:/Users/jyvin/OneDrive/Documents/GitHub/pyarchive/template2.xlsx"
        }
    ]
    }
```

V 0.3 (March 2022)
