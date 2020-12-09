import os
import json
from ui import creat_statistic_ui

def enter_directory():
    while True:
        path_to_directory = input("Enter directory: ")
        if os.path.isdir(path_to_directory):
            return path_to_directory
        else:
            print("Path is not a directory!")

def get_file_extension_statistics(extensions , files , size ,extensions_wanted ):
    for file in files:
        filename, file_extension = os.path.splitext(file["path"])
        if file_extension in extensions_wanted or (len(extensions_wanted) == 1 and extensions_wanted[0] == ''):
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
            size_percent = (value["size"]*100)/total_size

        if total_files == 0:
            count_percent = 0
        else:
            count_percent = (value["count"]*100)/total_files

        statistics.append({
            "size_percent":size_percent,
            "count_percent":count_percent,
            "extension":attr,
            "size":value["size"],
            "count":value["count"]
        })

    return  statistics

def get_extension_statistics_wanted(statistics,ext):
    my_json = {}
    answer = []
    for statistic in statistics:
        if statistic["extension"] in ext:
           my_json[statistic["extension"]] = statistic

    for e in ext:
        if e in my_json.keys():
            answer.append(my_json[e])
        else:
            answer.append({
                "count":0,
                "count_percent":0,
                "size":0,
                "size_percent":0,
                "extension":e
            })

    return answer

def get_directory_content_json_form(directory,json_format,extensions_wanted):
    json_format["files"] = []
    json_format["size"] = 0
    json_format["files_number"] = 0
    json_format["folders_number"] = 0
    json_format["files_extensions_statistics"] = {}

    files = os.listdir(directory)
    for file in files:
        path = ("%s\%s" % (directory,file))
        if os.path.isdir(path):
            json_format["folders_number"] += 1
            json_format[path] = get_directory_content_json_form(path,{},extensions_wanted)
            json_format["size"] += json_format[path]["size"]
            json_format["files"] += json_format[path]["files"]
            json_format["folders_number"] += json_format[path]["folders_number"]

        else:
            size = os.path.getsize(path)
            json_format["files"].append({"path":path,"size":size})
            json_format["size"] += size

    json_format["files_extensions_statistics"] = get_file_extension_statistics({},json_format["files"],json_format["size"],extensions_wanted)
    json_format["files_number"] = len(json_format["files"])

    return json_format

directory = "E:\Facultate 3"
extensions = "".split(",")

json_resulted = get_directory_content_json_form(directory,{},extensions)
json_object = json.dumps(json_resulted, indent = 4)

with open(directory.split('\\')[-1]+".json", "w") as outfile:
    outfile.write(json_object)


creat_statistic_ui(json_resulted["files_extensions_statistics"], "count_percent")
creat_statistic_ui(json_resulted["files_extensions_statistics"], "size_percent")

