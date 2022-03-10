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


def replace_global_parameter(value, g_row):
    # find all [[xxx]] and replace by g_row[xxx]
    gnames = get_global_names(value)

    for name in gnames:
        column = name.replace('[[','').replace(']]','')
        value =  value.replace(name, g_row[column])

    return value
    #if
#def
