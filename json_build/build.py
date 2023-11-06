import json
import os

class JSON_Object:
    def __init__(self, outer=None):
        self.__outer = outer if isinstance(outer, list) else None
        self.__master_dict = {}
        self.__master_json = {}
        self.__created = False

    '''
    This function updates the object model's __master_dict attr with the data needed to create the JSON object
    '''
    def add_object(self, unique_name, keyword, data, parent=None):
        unique_name = unique_name.strip()
        keyword = keyword.strip()
        if not isinstance(data, dict) and not isinstance(data, list):
            raise ValueError(f"Data must be of type dict or list, not {type(data)}")
        if not unique_name in self.__master_dict.keys():
            self.__master_dict[unique_name] = {
                "keyword": keyword,
                "data": data,
                "parent": parent,
                "children": []
            }

            if parent:
                self.__master_dict[parent]["children"].append(unique_name)
        else:
            raise ValueError(f"Unique name '{unique_name}' already exists")
        
    '''
    This function creates the object model's __master_json attr (Python dict) and dumps that dict into a JSON object
    '''

    def update_data(self, unique_name, new_data, reset_data=False):
        if not isinstance(new_data, dict) and not isinstance(new_data, list):
            raise ValueError(f"Data must be of type dict or list, not {type(new_data)}")
        elif unique_name not in self.__master_dict.keys():
            raise ValueError(f"Unique name '{unique_name}' does not exist")
        else:
            if isinstance(new_data, dict):
                if not isinstance(self.__master_dict[unique_name]["data"], dict):
                    raise ValueError(f"Data must be of type dict, not {type(self.__master_dict[unique_name]['data'])}")
                else:
                    if reset_data:
                        self.__master_dict[unique_name]["data"] = new_data
                    else:
                        self.__master_dict[unique_name]["data"].update(new_data)
            elif isinstance(new_data, list):
                if not isinstance(self.__master_dict[unique_name]["data"], list):
                    raise ValueError(f"Data must be of type list, not {type(self.__master_dict[unique_name]['data'])}")
                else:
                    if reset_data:
                        self.__master_dict[unique_name]["data"] = new_data
                    else:
                        self.__master_dict[unique_name]["data"].extend(new_data)


    def create(self, collapse=False, trim=False):
        if not self.__created: # This ensures that the master_json dict creation only happens once
            self.__created = True
            for _, value in self.__master_dict.items():
                if value["parent"]:
                    # How to handle if parent of object is a list
                    if isinstance(self.__master_dict[value["parent"]]["data"], list):
                        if value["data"] not in self.__master_dict[value["parent"]]["data"]: # If dict object is not already in the list (no dupes)
                            self.__master_dict[value["parent"]]["data"].append(value["data"])

                    # How to handle if parent of object is a dict
                    else:
                        if value["keyword"] not in self.__master_dict[value["parent"]]["data"].keys():
                            self.__master_dict[value["parent"]]["data"][value["keyword"]] = value["data"]
                        else:
                            raise ValueError(f"You are trying to add a duplicate keyword ('{value['keyword']}'). Please change one of the keywords.")
                else:
                    self.__master_json[value["keyword"]] = value["data"]
        to_dump = [self.__master_json] if isinstance(self.__outer, list) else self.__master_json
        
        if trim:
            def remove_null_empty_values(data):
                if isinstance(data, dict):
                    data_copy = data.copy()
                    for key, value in data_copy.items():
                        if value is None:
                            del data[key]
                        elif isinstance(value, (list, dict)):
                            cleaned_value = remove_null_empty_values(value)
                            if not cleaned_value:
                                del data[key]
                            else:
                                data[key] = cleaned_value
                    return data
                elif isinstance(data, list):
                    data_copy = data.copy()
                    for item in data_copy:
                        if item is None:
                            data.remove(item)
                        elif isinstance(item, (list, dict)):
                            cleaned_item = remove_null_empty_values(item)
                            if not cleaned_item:
                                data.remove(item)
                            else:
                                data[data.index(item)] = cleaned_item
                    return data
                else:
                    return data
                
            to_dump = remove_null_empty_values(to_dump)
        
        if collapse:
            return json.dumps(to_dump)
        else:    
            return json.dumps(to_dump, indent=4)
    

    '''
    This function calls the create() method, then saves the returned JSON object to a file
    '''
    def save(self, file_name, location_path=None):
        if not file_name.endswith('.json'):
            file_name = file_name.split('.')[0] + '.json'
        if location_path and not os.path.exists(location_path):
            os.makedirs(location_path)        
            file_path = os.path.join(location_path, file_name)
        else:
            file_path = file_name

        with open(file_path, 'w') as f:
            f.write(self.create())