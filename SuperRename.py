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
    MIDDLEFIX = middlefix_var.get()
    if MIDDLEFIX == "others":
        MIDDLEFIX = entry_middlefix.get()
    elif MIDDLEFIX == "space":
        MIDDLEFIX = " "
    else:
        if var1.get() == 1:
            MIDDLEFIX = " " + MIDDLEFIX + " "
    try:
        COUNT = int(entry_count.get())
    except ValueError:
        messagebox.showerror("Error", "Postfix must be a natural number.")
        return
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

def update_middlefix(*args):
    if middlefix_var.get() == "others":
        entry_middlefix.config(state="normal")
        check1.config(state="disabled")
    elif middlefix_var.get() == "space":
        entry_middlefix.config(state="disabled")
        check1.config(state="disabled")
    else:
        entry_middlefix.config(state="disabled")
        check1.config(state="normal")

files_to_ignore = ['00_rename_multi_files.py', 'README.md']
folder_to_ignore = ['.git']
extension_to_ignore = ['.git']

root = tk.Tk()
root.geometry("800x600")  # Set the initial size of the window
root.resizable(True, True)  # Make the window resizable

medium_font = ('Verdana',14)
large_font = ('Verdana',20)

label_prefix = tk.Label(root, text="Enter a prefix:", font=medium_font, anchor='w')
label_prefix.pack(fill='x', padx=10, pady=5)
entry_prefix = tk.Entry(root, font=medium_font)
entry_prefix.insert(0, "prefix")  # Set the default value for prefix
entry_prefix.pack(fill='x', padx=10, pady=5)

middlefix_frame = tk.Frame(root)
middlefix_frame.pack(fill='x', padx=10, pady=5)
label_middlefix = tk.Label(middlefix_frame, text="Choose a middlefix:", font=medium_font, anchor='w')
label_middlefix.pack(side='left')
middlefix_var = tk.StringVar(root)
middlefix_var.set("-")  # Set the default value for middlefix
middlefix_var.trace("w", update_middlefix)
middlefix_options = ["-", "_", "space", "others"]
middlefix_dropdown = tk.OptionMenu(middlefix_frame, middlefix_var, *middlefix_options)
middlefix_dropdown.config(font=large_font)
middlefix_dropdown.pack(side='left')
var1 = tk.IntVar()
check1 = tk.Checkbutton(middlefix_frame, text="Add space", variable=var1, state="normal")
check1.pack(side='left')
entry_middlefix = tk.Entry(root, font=medium_font, state="disabled")
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
