from collections import OrderedDict
import json
import os

class JSON_Object:
    def __init__(self):
        self.master_data = OrderedDict()

    """
    Takes in a JSON object or location and loads it into the master_data dictionary
    """
    def load(self, json_object=None, json_location=None):
        if not json_location and not json_object:
            raise Exception('No JSON object or location provided')
        elif json_object and json_location:
            raise Exception('Cannot provide both JSON object and location')
        elif json_object:
            if isinstance(json_object, dict):
                data = json_object
            elif isinstance(json_object, str):
                try:
                    data = json.loads(json_object)
                except:
                    raise Exception('Invalid JSON object')
        elif json_location:
            conditions = [
                os.path.exists(json_location),
                os.path.isfile(json_location),
                json_location.endswith('.json')
            ]
            if all(conditions):
                with open(json_location, 'r') as f:
                    data = json.load(f)
            else:
                raise Exception('Invalid JSON location or not a JSON file')
        def transform_to_tuple_keys(input_dict):
            output_dict = {}
            def traverse_dict(d, keys=()):
                for key, value in d.items():
                    new_keys = keys + (key,)
                    if isinstance(value, dict) and value:
                        traverse_dict(value, new_keys)
                    else:
                        output_dict[new_keys] = value
            traverse_dict(input_dict)
            return output_dict
        flat_dict = transform_to_tuple_keys(data)
        for k,v in flat_dict.items():
            unique_name = '_'.join(k)
            self.master_data[unique_name] = {}
            self.master_data[unique_name]['location'] = k
            self.master_data[unique_name]['category'] = k[1]
            self.master_data[unique_name]['keyword'] = k[-1]
            self.master_data[unique_name]['data'] = v
            self.master_data[unique_name]['show'] = False

    """
    Adds a new entry to the master_data dictionary
    """
    def add(self, unique_name, keyword, data, parent=None):
        unique_name = unique_name.lower().strip()
        keyword = keyword.lower().strip()

        if not unique_name in self.master_data.keys():
            self.master_data[unique_name] = {}

            if parent:
                if not parent in self.master_data.keys():
                    raise Exception(f'Parent ({parent}) does not exist')
                else:
                    parent = parent.lower().strip()
                    self.master_data[unique_name]['location'] = self.master_data[parent]['location'] + (unique_name,)
            else:
                self.master_data[unique_name]['location'] = (unique_name,)            
            
            
            self.master_data[unique_name]['keyword'] = keyword
            self.master_data[unique_name]['data'] = data
        else:
            raise Exception('Unique name already exists')

    """
    Updates an existing entry in the master_data dictionary
    """   
    def update(self, unique_name, data, reset=False):
        unique_name = unique_name.lower().strip()
        if unique_name in self.master_data.keys():
            if isinstance(self.master_data[unique_name]['data'], list):
                if not isinstance(data, list):
                    raise Exception('Data must be a list')
                else:
                    if reset:
                        self.master_data[unique_name]['data'] = data
                    else:
                        self.master_data[unique_name]['data'].extend(data)
            elif isinstance(self.master_data[unique_name]['data'], dict):
                if not isinstance(data, dict):
                    raise Exception('Data must be a dict')
                else:
                    if reset:
                        self.master_data[unique_name]['data'] = data
                    else:
                        self.master_data[unique_name]['data'].update(data)
            elif isinstance(self.master_data[unique_name]['data'], str):
                if not isinstance(data, str):
                    raise Exception('Data must be a str')
                else:
                    self.master_data[unique_name]['data'] = data
            elif isinstance(self.master_data[unique_name]['data'], int):
                if not isinstance(data, int):
                    raise Exception('Data must be a int')
                else:
                    self.master_data[unique_name]['data'] = data
        else:
            raise Exception('Unique name does not exist')
        
    """
    Uses the master_data dictionary to create a JSON object
    """
    def create(self, collapse=False, master_data=None):
        if master_data:
            if isinstance(master_data, dict):
                self.master_data = master_data
            else:
                raise Exception('Master data must be a dict')
        new_dict = OrderedDict()
        current_dict = new_dict
        for _,v in self.master_data.items():
            if v['show']:
                for item in v['location'][:-1]:
                    if not item in current_dict.keys():
                        current_dict[item] = {}
                    current_dict = current_dict[item]
                current_dict[v['location'][-1]] = v['data']
                current_dict = new_dict
        to_dump = new_dict

        # if trim:
        #     def remove_null_empty_values(data):
        #         if isinstance(data, dict):
        #             data_copy = data.copy()
        #             for key, value in data_copy.items():
        #                 if value is None:
        #                     del data[key]
        #                 elif isinstance(value, (list, dict)):
        #                     cleaned_value = remove_null_empty_values(value)
        #                     if not cleaned_value:
        #                         del data[key]
        #                     else:
        #                         data[key] = cleaned_value
        #             return data
        #         elif isinstance(data, list):
        #             data_copy = data.copy()
        #             for item in data_copy:
        #                 if item is None:
        #                     data.remove(item)
        #                 elif isinstance(item, (list, dict)):
        #                     cleaned_item = remove_null_empty_values(item)
        #                     if not cleaned_item:
        #                         data.remove(item)
        #                     else:
        #                         data[data.index(item)] = cleaned_item
        #             return data
        #         else:
        #             return data
        #     to_dump = remove_null_empty_values(to_dump)

        if collapse:
            return json.dumps(to_dump)
        else:    
            return json.dumps(to_dump, indent=4)
        
    """
    Calls the create() function to create a JSON object, then the JSON object to a file locally
    """
    def save(self, filename, location_path=None, trim=False):
        if not filename.endswith('.json'):
            filename = filename.split('.')[0] + '.json'
        if location_path and not os.path.exists(location_path):
            os.makedirs(location_path)        
            file_path = os.path.join(location_path, filename)
        else:
            file_path = filename

        with open(file_path, 'w') as f:
            f.write(self.create(trim=trim))