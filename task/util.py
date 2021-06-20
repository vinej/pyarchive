def get_dict_value(data, name):
    if name in data:
        return data[name]
    elif name.lower() in data:
        return data[name.lower()]
    else:
        return None
    #if
#def
