## imports
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from pathlib import Path
import os
from Deduper import hash_file, collect_files, find_duplicates, scan_for_duplicates, delete_duplicates

## start app
root = tk.Tk()
root.title('Duplicate Remover')
root.geometry('600x400')

## Parameters
folder_path = None
last_scan_for_duplicates = None

## GUI Functions
def select_folder():
    """select a folder using file explorer"""
    global folder_path
    folder = filedialog.askdirectory()
    if folder:
        folder_path = Path(folder)
        output_text.delete('1.0', tk.END)  ## only way to wipe the logs
        clickable_folder()

def clickable_folder():
    if folder_path is None:
        return

    output_text.insert(tk.END, 'This folder has been selected\n')
    start = output_text.index('insert')
    output_text.insert(tk.END, f"{folder_path}\n")
    end = output_text.index('insert')

    tag = 'folder_link'
    output_text.tag_add(tag, start, end)
    output_text.tag_config(tag, foreground='blue', underline=True)
    output_text.tag_bind(tag, '<Button-1>', lambda e: os.startfile(folder_path))
    output_text.tag_bind(tag, '<Enter>', lambda e: output_text.config(cursor='hand2'))
    output_text.tag_bind(tag, '<Leave>', lambda e: output_text.config(cursor=''))
    output_text.insert(tk.END, '\n')


def scan_folder():
    """scan selected folder for duplicates"""
    output_text.insert(tk.END, '\n')

    if folder_path is None:
        output_text.insert(tk.END, 'please select a folder first\n')
        return
    
    output_text.insert(tk.END, f"Scanning folder: {folder_path} and all subfolders\n")
    output_text.see(tk.END)
    output_text.update_idletasks()

    skipped_count = 0

    try:
        global last_scan_for_duplicates
        last_scan_for_duplicates = scan_for_duplicates(folder_path)
        duplicates = last_scan_for_duplicates
        output_text.insert(tk.END, 'scan completed \n')

        if not duplicates:
            output_text.insert(tk.END, 'no duplicates found\n')
        else:
            originals_with_duplicates = len(duplicates)
            duplicates_with_originals = sum(len(entry['duplicates']) for entry in duplicates)
            total_size_of_duplicates = sum(f.stat().st_size for entry in duplicates for f in entry['duplicates'])
            if total_size_of_duplicates >=1024**3:
                total_size_of_duplicates_output = f"{total_size_of_duplicates / 1024**3:.2f} GB\n"
            else:
                total_size_of_duplicates_output = f"{total_size_of_duplicates / 1024**2:.2f} MB\n"
            output_text.insert( tk.END,
                                f'{originals_with_duplicates} original files that have duplicates\n'
                                f'have a total of {duplicates_with_originals} duplicate files\n'
                                f'with a total size of {total_size_of_duplicates_output}\n')

        if skipped_count >0:
            output_text.insert(tk.END, f'{skipped_count} files were skipped due to errors\n')
        
        output_text.see(tk.END)

    except Exception as e:
        output_text.insert(tk.END, f'Fatal error scanning folder: {e}\n')
        output_text.see(tk.END)

def delete_all_duplicates():
    """Delete all duplicates from last scan"""
    if folder_path is None:
        output_text.insert(tk.END, 'Please select a folder first.\n')
        return
    
    if not last_scan_for_duplicates:
        output_text.insert(tk.END, 'No scan results found.  Run a scan first.\n')
        return
    
    ##confirmation
    confirm = messagebox.askyesno('Confirm Deletion of Duplicate Files', 'Are you sure you want to delete all duplicate files from the last scan?')
    if not confirm:
        output_text.insert(tk.END, 'Deletion canceled by user\n')
        return
    
    files_deleted = 0
    bytes_deleted = 0

    for entry in last_scan_for_duplicates:
        for f in entry['duplicates']:
            try:
                bytes_deleted += f.stat().st_size
                files_deleted +=1
            except Exception as e:
                pass
    if bytes_deleted >= 1024**3:
        bytes_deleted_str = f"{bytes_deleted / 1024**3:.2f} GB\n"
    else:
        bytes_deleted_str = f"{bytes_deleted / 1024**2:.2f} MB\n"

    output_text.insert(tk.END, 'Starting to delete duplicate files.\n')
    output_text.update_idletasks()

    try:
        delete_duplicates(last_scan_for_duplicates)
        output_text.insert( tk.END,
                            f'deleted {files_deleted} duplicate files\n'
                            f'which freed {bytes_deleted_str}')
    except Exception as e:
        output_text.insert(tk.END, 'error deleting duplicates, {e}\n')
    
    output_text.see(tk.END)

## GUI
select_folder_button = tk.Button(root, text='Select Folder', command = select_folder)
select_folder_button.pack(pady=10)

scan_button = tk.Button(root, text='Scan folder for duplicates', command = scan_folder)
scan_button.pack(pady=10)

delete_button = tk.Button(root, text = 'Delete All Duplicates', command = delete_all_duplicates)
delete_button.pack(pady=10)

output_text = tk.Text(root, wrap=tk.WORD, height=15)
output_text.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

##app run
root.mainloop()

##TODO: lags due to not being multithreaded.  Shows at not responding when executing function call
##TODO: add in some kind of progress bar to show that it is still running and not stuck
##TODO: make folder clickable in all instances, not just first instance
##TODO: add progress bar