import json
import os

class JSON_Object:
    def __init__(self, outer=None):
        self.outer = outer if isinstance(outer, list) else None
        self.master_dict = {}
        self.master_json = {}

    def add_object(self, unique_name, keyword, data, parent=None):
        unique_name = unique_name.strip()
        keyword = keyword.strip()
        if not isinstance(data, dict) and not isinstance(data, list):
            raise ValueError(f"Data must be of type dict or list, not {type(data)}")
        if not unique_name in self.master_dict.keys():
            self.master_dict[unique_name] = {
                "keyword": keyword,
                "data": data,
                "parent": parent,
                "children": []
            }

            if parent:
                self.master_dict[parent]["children"].append(unique_name)
        else:
            raise ValueError(f"Unique name '{unique_name}' already exists")
        
    def create(self):
        for _, value in self.master_dict.items():
            if value["parent"]:
                if isinstance(self.master_dict[value["parent"]]["data"], list):
                    if value["data"] not in self.master_dict[value["parent"]]["data"]:
                        self.master_dict[value["parent"]]["data"].append(value["data"])
                else:
                    if value["data"] not in self.master_dict[value["parent"]]["data"].values():
                        self.master_dict[value["parent"]]["data"][value["keyword"]] = value["data"]
            else:
                self.master_json[value["keyword"]] = value["data"]
            to_dump = [self.master_json] if isinstance(self.outer, list) else self.master_json            
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