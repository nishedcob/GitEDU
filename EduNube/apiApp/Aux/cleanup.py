

def clean_dict(entry_dict):
    for key, value in entry_dict.items():
        if type(value) == dict:
            entry_dict[key] = clean_dict(entry_dict=value)
        elif type(value) == tuple:
            entry_dict[key] = clean_list(list(value))
        elif type(value) == list:
            entry_dict[key] = clean_list(value)
        elif type(value) == bytes:
            entry_dict[key] = value.decode("utf-8")
    return entry_dict


def clean_list(entry_list):
    for index in range(len(entry_list)):
        value = entry_list[index]
        if type(value) == dict:
            entry_list[index] = clean_dict(value)
        elif type(value) == tuple:
            entry_list[index] = clean_list(list(value))
        elif type(value) == list:
            entry_list[index] = clean_list(value)
        elif type(value) == bytes:
            entry_list[index] = value.decode("utf-8")
    return entry_list
