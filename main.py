import os
import json

def enter_directory():
    while True:
        path_to_directory = input("Enter directory: ")
        if os.path.isdir(path_to_directory):
            return path_to_directory
        else:
            print("Path is not a directory!")

def get_directory_content_json_form(directory,json_format):
    json_format["files"] = []
    files = os.listdir(directory)
    for file in files:
        if file[0] == "." :
            continue
        path = f'{directory}\{file}'
        if os.path.isdir(path):
            json_format[file] = get_directory_content_json_form(path,{})
        else:
            json_format["files"].append(file)

    return json_format


my_json = get_directory_content_json_form('E:\Facultate 3\FolderToJson',{})
json_string = json.dumps(my_json)
parsed = json.loads(json_string)
print(json.dumps(parsed, indent=4, sort_keys=True))