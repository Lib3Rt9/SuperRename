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
    MIDDLEFIX = entry_middlefix.get()
    COUNT = int(entry_count.get())
    path = pathlib.Path(directory)
    items_set = set(chain(files_to_ignore, folder_to_ignore, extension_to_ignore))

    os.chdir(path)
    renamed_files = 0
    for file in os.listdir():
        if file not in items_set:
            file_name, file_ext = os.path.splitext(file)
            file_name = PREFIX + MIDDLEFIX + str(COUNT)
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
    label_last_process.config(text=f"Last renaming process renamed {last_renamed_files} files in the directory:\n{last_renamed_directory}")
    messagebox.showinfo("Success", f"Renaming process completed successfully. {renamed_files} files were renamed.")

def browse_directory():
    global directory
    directory = filedialog.askdirectory()
    label_directory.config(text=directory)

files_to_ignore = ['00_rename_multi_files.py', 'README.md']
folder_to_ignore = ['.git']
extension_to_ignore = ['.git']

root = tk.Tk()
root.geometry("800x600")  # Set the initial size of the window
root.resizable(True, True)  # Make the window resizable

medium_font = ('Verdana',14)

label_prefix = tk.Label(root, text="Enter a prefix:", font=medium_font, anchor='w')
label_prefix.pack(fill='x', padx=10, pady=5)
entry_prefix = tk.Entry(root, font=medium_font)
entry_prefix.insert(0, "prefix")  # Set the default value for prefix
entry_prefix.pack(fill='x', padx=10, pady=5)

label_middlefix = tk.Label(root, text="Enter a middlefix:", font=medium_font, anchor='w')
label_middlefix.pack(fill='x', padx=10, pady=5)
entry_middlefix = tk.Entry(root, font=medium_font)
entry_middlefix.insert(0, "-")  # Set the default value for middlefix
entry_middlefix.pack(fill='x', padx=10, pady=5)

label_count = tk.Label(root, text="Enter starting number:", font=medium_font, anchor='w')
label_count.pack(fill='x', padx=10, pady=5)
entry_count = tk.Entry(root, font=medium_font)
entry_count.insert(0, "0")  # Set the default value for postfix
entry_count.pack(fill='x', padx=10, pady=5)

button_browse = tk.Button(root, text="Browse", command=browse_directory, font=medium_font, bg='light blue')
button_browse.pack(fill='x', padx=10, pady=5)
label_directory = tk.Label(root, text="", font=medium_font, wraplength=700, anchor='w')
label_directory.pack(fill='x', padx=10, pady=5)

button_rename = tk.Button(root, text="Rename Files", command=rename_files, font=medium_font, bg='light green')
button_rename.pack(fill='x', padx=10, pady=5)

label_last_process = tk.Label(root, text="", font=medium_font, wraplength=700, anchor='w')
label_last_process.pack(fill='x', padx=10, pady=5)

root.mainloop()
