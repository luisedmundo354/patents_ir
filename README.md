# SAUL Patent Processing and Indexing Module

## Overview

This repository provides tools for parsing, preprocessing, and indexing US patent documents in XML format. It includes capabilities to transform XML patents into JSON format, visualize these patents, and maintain an index for easy access and manipulation of patent groups.

** The patents in json format go inside json_patents**

** The patents in xml format go inside xml_tatents_wn **

## Functions

### 1. XML Processing

#### `process_xml_file`

- **Input**: Path to an XML file containing patents (`e.g., patents/ipg080729.xml`).
- **Output**: Individual XML files for each patent in a specified directory.

This function splits a bulk XML file with multiple patents into separate XML files for easier management and processing.

### 2. Patent Visualization

#### `print_patent`

- **Input**: Path to an individual XML patent file (`e.g., xml_patents_wn/07404685.xml`).
- **Output**: Printed representation of the patent for visualization.

This function allows users to view the contents of a patent in a readable format.

### 3. JSON Conversion

#### `extract_and_convert_to_json`

- **Input**: Path to a single XML patent file.
- **Output**: JSON formatted string and a patent object of type `Patent`.

This function extracts data from XML and converts it into JSON format, including the transformation into a custom patent dataclass.

#### `json_to_patent`

- **Input**: JSON string formatted patent data.
- **Output**: A patent object of type `Patent`.

This function translates JSON formatted patents back into dataclass objects, facilitating further manipulations in Python.

### 4. Dataclasses

#### `InternationalClassification`

Represents international patent classification details. 

- **Functions**:
  - `to_dict()`: Converts the classification to a dictionary form. 

#### `Claims`

Structures data about patent claims.

- **Functions**:
  - `add_component()`: Adds components and subcomponents to claims.
  - `to_dict()`: Converts claims to dictionary form.

#### `Patent`

A comprehensive structure encapsulating patent details.

- **Functions**:
  - `to_json()`: Serializes the patent information to a JSON formatted string.

### 5. Patent Indexing

#### `initialize_index`

- **Input**: Path to the JSON index file.
- **Output**: Initializes a JSON file for patent indexing.

Creates an empty structure, if none exists, to store patent groupings for indexed operations.

#### `load_index`

- **Input**: Path to the JSON index file.
- **Output**: Loaded index in a dictionary format.

Loads an existing index from the file for manipulation.

#### `add_group`

- **Input**: The index dictionary, JSON file path, and group name.
- **Output**: Adds a new patent group to the index.

Enables creation of new organizations of patents under specified group names.

#### `add_element_to_group`

- **Input**: Index dictionary, JSON file path, group name, and patent number.
- **Output**: Appends a patent number to a group.

This function supports adding patents to existing groups for collective management.

#### `remove_element_from_group`

- **Input**: Index dictionary, JSON file path, group name, and patent number.
- **Output**: Removes a patent number from a specified group.

Allows removal of miscategorized or unwanted patents from groups.

#### `retrieve_group_elements`

- **Input**: Index dictionary and patent number.
- **Output**: Patent numbers in the specified group and the group name.

Facilitates retrieval of all patents within a group sharing a common patent number.

#### `remove_group`

- **Input**: Index dictionary, JSON file path, and group name.
- **Output**: Deletes a specified group from the index.

Allows complete deletion of a group and its associated records.

### Patent Index

The index contains collections of patent numbers organized into groups for efficient access and retrieval. The groups are list values and the group names are the keys of the dictionary.

### To use azure

pip install azure-ai-inference