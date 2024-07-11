import os
import pathlib
import glob
from itertools import chain

path = pathlib.Path(__file__).parent.resolve()
files_to_ignore = ['00_rename_multi_files.py', 'README.md']
folder_to_ignore = ['.git']
extension_to_ignore = ['.git']
items_set = set(chain(files_to_ignore, folder_to_ignore, extension_to_ignore))

PREFIX = input("Enter a prefix: ")
COUNT = int(input("Enter starting number: "))

print(path)

# place the all willing-to-rename files and this z1.py file into the same folder
os.chdir(path)                # change this path to where this file is located
print(os.getcwd())

#function to increment count to make the files sorted0
def increment():
    global COUNT
    COUNT = COUNT + 1

for file in os.listdir():
    # for file in glob.glob(os.listdir()):
    if file not in items_set:
        file_name, file_ext = os.path.splitext(file)
        file_name = PREFIX + str(COUNT)                 # "000" is the prefix, change to whatever is ok, then the suffix is the number incresing from the COUNT in line 6
        
        increment()
        
        new_name = '{}{}'.format(file_name, file_ext)
        os.rename(file, new_name)
