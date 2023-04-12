import csv

def dictionary_from_csv(csv_file, key_description =  'key', value_description = 'value'):
    with open(csv_file, 'r') as csv_to_dict:
        data_object = csv.reader(csv_to_dict)
        header_list = next(data_object)
        key_index = header_list.index(key_description)
        value_index = header_list.index(value_description)
        data_dictionary = {row[key_index]: row[value_index] for row in data_object}

    return data_dictionary
