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
