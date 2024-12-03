import json
import os

def initialize_index(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as index_file:
            json.dump({}, index_file, indent=4)
        print("Your index has been created!")
    else:
        print("The index has already been initialized")

# Load the index file
def load_index(file_path):
    with open(file_path, 'r') as index_file:
        return json.load(index_file)

# Save the index to the file
def save_index(index, file_path):
    with open(file_path, 'w') as index_file:
        json.dump(index, index_file, indent=4)

def add_group(index, file_path, group_name):
    if group_name not in index:
        index[group_name] = []
        save_index(index, file_path)

# Add an element to a group and save immediately
def add_element_to_group(index, file_path, group_name, element):
    if group_name in index:
        if element not in index[group_name]:
            index[group_name].append(element)
            save_index(index, file_path)
    else:
        index[group_name] = [element]
        save_index(index, file_path)

# Remove an element from a group and save immediately
def remove_element_from_group(index, file_path, group_name, element):
    if group_name in index:
        if element in index[group_name]:
            index[group_name].remove(element)
            save_index(index, file_path)

def remove_group(index, file_path, group_name):
    if group_name in index:
        del index[group_name]
        save_index(index, file_path)

# Retrieve elements of a group given one of the elements
def retrieve_group_elements(index, element):
    for group_name, elements in index.items():
        if element in elements:
            return elements, group_name
        else:
            print("The patent is not in the index!")
    return []