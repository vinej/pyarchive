'''
    return an object from of json object
    return None if the object does not exist
'''
def get_dict_value(data, name):
    if name in data:
        return data[name]
    elif name.lower() in data:
        return data[name.lower()]
    else:
        return None
    #if
#def

def get_global_names(value):
    outnames = []
    # return a list of name {{xxx}}
    list = str(value).split('[[')
    for part in list:
        idx = part.find(']]')
        if idx != -1:
            outnames.append('[['+part[:idx+2])
    return outnames
#def


'''
    g_rows is a map of 3 grows
        { name:rows, name:rows, name:rows }
    Global parameters have the format [[name.column]]

'''
def replace_global_parameter(value, g_rows):
    # find all [[name.column]] and replace by g_rows[name][column]
    if g_rows == None:
        return value
    #if
    gnames = get_global_names(value)

    for name in gnames:
        gparam = name.replace('[[','').replace(']]','')
        onename,column = gparam.split('.')
        value =  value.replace('[['+gparam+']]',g_rows[onename][column])

    return value
#def

def read_csv(value):
    rows = []
    columns = []
    # displaying the contents of the CSV file
    first = True
    for row in value:
        if first:
            columns = row
            first = False
        else :
            onerow = {}
            for i in range(len(columns)):
                onerow[columns[i]] = row[i]
            #for
            rows.append(onerow)
        #if
    #for
    return columns, rows
#def

import json
"""
read a json file with the format 
    [
        {},
        {},
        {}....
    ]
"""
def read_json(value):
    rows = []
    columns = []
    jvalue = json.loads(value)
    # displaying the contents of the CSV file
    first = True
    for row in jvalue:
        if first:
            for k in row:
                columns.append(k)
            first = False
        #if

        onerow = {}
        for k,v in row.items():
            onerow[k] = v
        #for
        rows.append(onerow)
    #for
    return columns, rows
#def

import xml.etree.ElementTree as ET
"""
read a xml file with the format
<root>
    <tag>
        <...>???</...>
        <...>???</...>
        <...>???</...>
        <...>???</...>
    </tag>
    <tag>
        <...>???</...>
        <...>???</...>
        <...>???</...>
        <...>???</...>
    </tag>
    <tag>
        <...>???</...>
        <...>???</...>
        <...>???</...>
        <...>???</...>
    </tag>
</root>
"""
def read_xml(value):
    rows = []
    columns = []
    # displaying the contents of the CSV file
    root = ET.fromstring(value)
    #root = tree.getroot()
    first = True
    #xrows = tree.getchildren()
    for row in root:
        if first:
            for child in row:
                columns.append(child.tag)
            first = False
        #if    
        onerow = {}
        for child in row:
            onerow[child.tag] = child.text
        #for
        rows.append(onerow)
    #for
    return columns, rows
#def

