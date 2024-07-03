import os
import pathlib
import glob
from itertools import chain
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

COUNT = 0
last_renamed_files = 0
last_renamed_directory = ""

def increment():
    global COUNT
    COUNT = COUNT + 1

def rename_files():
    global COUNT, last_renamed_files, last_renamed_directory
    PREFIX = entry_prefix.get()
    COUNT = int(entry_count.get())
    path = pathlib.Path(directory)
    items_set = set(chain(files_to_ignore, folder_to_ignore, extension_to_ignore))

    os.chdir(path)
    renamed_files = 0
    for file in os.listdir():
        if file not in items_set:
            file_name, file_ext = os.path.splitext(file)
            file_name = PREFIX + str(COUNT)
            increment()
            new_name = '{}{}'.format(file_name, file_ext)
            try:
                os.rename(file, new_name)
                renamed_files += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file {file}. Error: {str(e)}")
                return
    last_renamed_files = renamed_files
    last_renamed_directory = directory
    messagebox.showinfo("Success", f"Renaming process completed successfully. {renamed_files} files were renamed.")

def browse_directory():
    global directory
    directory = filedialog.askdirectory()
    label_directory.config(text=directory)

def show_last_process():
    messagebox.showinfo("Last Process", f"Last renaming process renamed {last_renamed_files} files in the directory {last_renamed_directory}.")

files_to_ignore = ['00_rename_multi_files.py', 'README.md']
folder_to_ignore = ['.git']
extension_to_ignore = ['.git']

root = tk.Tk()

label_prefix = tk.Label(root, text="Enter a prefix:")
label_prefix.pack()
entry_prefix = tk.Entry(root)
entry_prefix.pack()

label_count = tk.Label(root, text="Enter starting number:")
label_count.pack()
entry_count = tk.Entry(root)
entry_count.pack()

button_browse = tk.Button(root, text="Browse", command=browse_directory)
button_browse.pack()
label_directory = tk.Label(root, text="")
label_directory.pack()

button_rename = tk.Button(root, text="Rename Files", command=rename_files)
button_rename.pack()

button_last_process = tk.Button(root, text="Show Last Process", command=show_last_process)
button_last_process.pack()

root.mainloop()
