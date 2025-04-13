from os import listdir
from os.path import isfile, join

def list_files_in_folder(file_path):
    return [f'{file_path}/{f}' for f in listdir(file_path) if isfile(join(file_path, f))]