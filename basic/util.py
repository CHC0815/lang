import os

PATH = "./lib/"


def searchFile(fileName):
    for dirpath, dirnames, filenames in os.walk(PATH):
        for filename in filenames:
            if filename == fileName:
                filename = os.path.join(dirpath, filename)
                return filename
    return None
