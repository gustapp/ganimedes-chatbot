def format_entity(concept_name):
    return '_'.join(concept_name.lower().split(' '))

def format_param(parameter):
    if parameter == '' or parameter == 'indiferente':
        return
    else:
        return parameter

def format_param_list(parameter):
    formatted_list = []
    for param in parameter:
        value = format_param(param)
        if value:
            formatted_list.append(value)
    return formatted_list