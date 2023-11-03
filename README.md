# json-build

json-build is a package that allows developers to build and save JSON files quickly.

## Installation

```python
pip install json-build
```

## Create a new JSON object to build upon

```python
from json_build import JSON_Object

new_json = JSON_Object(outer=[])

# 'outer' argument is optional
# if 'outer=[]' is passed it will wrap the JSON object in an array (Python list)
# otherwise, it will be a JSON object (Python dictionary)
```

## Nest objects inside the JSON object

```python
new_json.add_object(
    unique_name="people", 
    keyword="people", 
    data={},
    )

new_json.add_object(
    unique_name = 'person_1',
    keyword = 'person1',
    data = {"first_name": "Michael", "last_name": "Myers"},
    parent='people',
)

new_json.add_object(
    unique_name = 'relative_1',
    keyword = 'relative',
    data = {"first_name": "Laurie", "last_name": "Strode", "relation": "Sister"},
    parent = 'person_1'
)

new_json.add_object(
    unique_name = 'person_2',
    keyword = 'person2',
    data = {"first_name": "Jason", "last_name": "Voorhees"},
    parent='people',
)

new_json.add_object(
    unique_name = 'relative_2',
    keyword = 'relative',
    data = {"first_name": "Pamela", "last_name": "Voorhees", "relation": "Mother"},
    parent = 'person_2'
)

new_json.add_object(
    unique_name = 'movies',
    keyword = 'movies',
    data = [
        'Halloween',
        'Friday the 13th',
        'Nightmare on Elm Street',
    ],
)

# 'parent' argument is optional; if unpassed, the object will be added to the JSON object's first level
# Note that 'parent' uses the unique_name of the parent object, and not the keyword
```

## Create the JSON object

```python
new_json.create()
```

## Save the JSON object to a file

```python
new_json.save(file_name="killer_names", location_path="C:/Users/fkrueger/Desktop/")

# 'location_path' argument is optional; if unpassed it will save the file to the root of your local project
```

## Resultant JSON object
```json
[
    {
        "people": {
            "person1": {
                "first_name": "Michael",
                "last_name": "Myers",
                "relative": {
                    "first_name": "Laurie",
                    "last_name": "Strode",
                    "relation": "Sister"
                }
            },
            "person2": {
                "first_name": "Jason",
                "last_name": "Voorhees",
                "relative": {
                    "first_name": "Pamela",
                    "last_name": "Voorhees",
                    "relation": "Mother"
                }
            }
        },
        "movies": [
            "Halloween",
            "Friday the 13th",
            "Nightmare on Elm Street"
        ]
    }
]
```