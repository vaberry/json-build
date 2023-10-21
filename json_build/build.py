import json
import os

class JSON_Object:
    def __init__(self, outer=None):
        self.__outer = outer if isinstance(outer, list) else None
        self.__master_dict = {}
        self.__master_json = {}
        self.__created = False

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
        
    def create(self):
        if not self.__created:
            self.__created = True
            for _, value in self.__master_dict.items():
                if value["parent"]:
                    # HOW TO HANDLE IF PARENT OF OBJECT IS A LIST
                    if isinstance(self.__master_dict[value["parent"]]["data"], list):
                        if value["data"] not in self.__master_dict[value["parent"]]["data"]: # If dict object is not already in the list (no dupes)
                            self.__master_dict[value["parent"]]["data"].append(value["data"])

                    # HOW TO HANDLE IF PARENT OF OBJECT IS A DICT
                    else:
                        if value["keyword"] not in self.__master_dict[value["parent"]]["data"].keys():
                            self.__master_dict[value["parent"]]["data"][value["keyword"]] = value["data"]
                        else:
                            raise ValueError(f"You are trying to add a duplicate keyword ('{value['keyword']}'). Please change one of the keywords.")
                else:
                    self.__master_json[value["keyword"]] = value["data"]
        to_dump = [self.__master_json] if isinstance(self.__outer, list) else self.__master_json     
        return json.dumps(to_dump, indent=4)
    
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