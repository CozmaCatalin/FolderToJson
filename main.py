import os
import json

def enter_directory():
    while True:
        path_to_directory = input("Enter directory: ")
        if os.path.isdir(path_to_directory):
            return path_to_directory
        else:
            print("Path is not a directory!")

def get_file_extension_statistics(extensions , files , size):
    for file in files:
        filename, file_extension = os.path.splitext(file["path"])
        if file_extension not in extensions:
            extensions[file_extension] = {}
            extensions[file_extension]["size"] = file["size"]
            extensions[file_extension]["count"] = 1
        else:
            extensions[file_extension]["size"] += file["size"]
            extensions[file_extension]["count"] += 1

    return get_statistics(extensions,size,len(files))

def get_statistics(extensions,total_size,total_files):
    statistics = []
    for attr, value in extensions.items():
        if total_size == 0:
            size_percent = 0
        else:
            size_percent = f'{(value["size"]*100)/total_size}%'

        if total_files == 0:
            count_percent = 0
        else:
            count_percent = f'{(value["count"]*100)/total_files}%'

        statistics.append({
            "size_percent":size_percent,
            "count_percent":count_percent,
            "extension":attr,
            "size":value["size"],
            "count":value["count"]
        })

    return  statistics

def get_directory_content_json_form(directory,json_format):
    json_format["files"] = []
    json_format["size"] = 0
    json_format["files_number"] = 0
    json_format["folders_number"] = 0
    json_format["files_extensions_statistics"] = {}

    files = os.listdir(directory)
    for file in files:
        path = f'{directory}\{file}'
        if os.path.isdir(path):
            json_format["folders_number"] += 1
            json_format[path] = get_directory_content_json_form(path,{})
            json_format["size"] += json_format[path]["size"]
            json_format["files"] += json_format[path]["files"]
            json_format["folders_number"] += json_format[path]["folders_number"]

        else:
            size = os.path.getsize(path)
            json_format["files"].append({"path":path,"size":size})
            json_format["size"] += size

    json_format["files_extensions_statistics"] = get_file_extension_statistics({},json_format["files"],json_format["size"])
    json_format["files_number"] = len(json_format["files"])

    return json_format

my_json = get_directory_content_json_form('E:\FITNESS-APP-FRONTEND',{})

print(str(my_json["size"]) + " bytes " + str(my_json["files_number"]) + " files " + str(my_json["folders_number"]) + " folders")
json_string = json.dumps(my_json["files_extensions_statistics"])
parsed = json.loads(json_string)
print(json.dumps(parsed, indent=4, sort_keys=True))