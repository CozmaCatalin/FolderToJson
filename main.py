import os

def enterDirectory():
    while True:
        pathToDirectory = input("Enter directory: ")
        if os.path.isdir(pathToDirectory):
            break
        else:
            print("Path is not a directory!")

enterDirectory()