import json 
import os

class JSON_Object:
    def __init__(self, outer=None):
        self.outer = outer if isinstance(outer, list) else {}
        self.parents = []
        self.unique_to_keyword_map = {} 
        self.child_to_parent_map = {}
        self.display_dict = {}
    
    def add_object(self, unique_name, keyword, data, parent=None):
        '''
        update the unique_to_keyword_map or raise error if unique_name already exists
        '''
        if not unique_name in self.unique_to_keyword_map.keys():
            self.unique_to_keyword_map[unique_name] = keyword
            if isinstance(data, dict):
                self.parents.append(unique_name)
            if parent:
                if parent in self.parents:
                    if parent in self.unique_to_keyword_map.keys():
                        self.child_to_parent_map[unique_name] = parent
                    else:
                        raise ValueError(f"Parent '{parent}' does not exist")
                else:
                    raise TypeError(f"Parent can only be a dict object. Options are: {self.parents}")
            else:
                self.child_to_parent_map[unique_name] = None
        else:
            raise ValueError(f"unique_name '{unique_name}' already exists")

        '''
        create the list of keys to navigate to the correct place in the display_dict
        e.g output = ['dictLevel 1', 'dictLevel 2', 'dictLevel 3']
        '''
        keys_list = [unique_name, parent] if parent else [unique_name]
        start_key = parent if parent else unique_name
        while self.child_to_parent_map.get(start_key) is not None:
            start_key = self.child_to_parent_map.get(start_key)
            if start_key is not None:
                keys_list.append(start_key)
            else:
                break

        '''
        create display dict for json dump
        '''
        dict_navigation = keys_list[::-1]
        current_dict = self.display_dict
        for key in dict_navigation[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]
        current_dict[dict_navigation[-1]] = data


    def save(self, file_name, location_path=None):
        if location_path and not os.path.exists(location_path):
            os.makedirs(location_path)        
            file_path = os.path.join(location_path, file_name)
        else:
            file_path = file_name

        to_dump = [self.display_dict] if isinstance(self.outer, list) else self.display_dict
        with open(file_path, 'w') as f:
            json.dump(to_dump, f, indent=4)