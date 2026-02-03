# Duplicate Remover

### Problem
Over time, digital files tend to accumulate which often results in unnecessary duplicates.  In my case, I had photos and videos from multiple old phones and devices scattered across different backups.  These duplicates consume significant storage space and make file management cumbersome.

### Solution
This program allows you to select a specific folder to clean and remove all nested duplicates within that folder, freeing up more space on your device.  
![Duplicate_File_Deleter_Pictures](https://github.com/user-attachments/assets/d8189e0a-5de1-4e79-8a5a-fa7c243095b8)  

## How it works


### Part 1: Select Folder  
Use the 'Select Folder' button to select the folder that you want to remove duplicates from.  The program can look at that folder and all subfolders and files underneath.  
You'll get a message in the textbox about the selected folder, and be able to click the blue text to open that folder in file explorer if you would like.  
![Duplicate_File_Deleter_Select_Folder](https://github.com/user-attachments/assets/67bcc6ec-3644-4094-81d3-363afd858cf3)  

### Part 2: Scan Folder For Duplicates  
Use the 'Scan Folder For Duplicates' button to scan the selected folder and subfolders for any duplicate files.  
>**File Hashes** This scan works by creating a **hash**, a unique identifier based on the content of the file.  If you make a duplicate of a file and rename it, the hash is still the same because the content of the file did not change.  Adding even a single space to a document will change its hash and make it not a duplicate.

You'll get a message of 'Scanning folder' when the scan starts.  
You'll also get a notification of how many duplicate files and their size were found.  If there are no duplicates it will return 'no duplicates found'  
>**Tip**: If it says 'Not Responding' it should still be working in the background on its task even if the GUI doesn't update.

![Duplicate_File_Deleter_Scan](https://github.com/user-attachments/assets/f59d97db-839c-4809-80ae-1b541f174a29)  

### Part 3: Delete All Duplicates  
Use the 'Delete All Duplicates' button to delete all duplicates that were found.  
>**Original Files** Determining which files is the 'original' is an interesting challenge.  Currently it is determined by the earliest creation time.  This does not work perfectly if the files were created at the same time, and I don't have additional logic such as prioritize files that do not contain -copy, -1, (1), _1

It will give an additional popup confirming that you would like to delete those files, so it is difficult to accidentally remove files.  You'll get a message in the text box that the process has started with 'Starting to delete duplicate files' if you confirm or 'Deletion cancelled by user' if you do not confirm.  
After it successfully deletes it will let you know how much space was freed up.  

![Duplicate_File_Deleter_Delete](https://github.com/user-attachments/assets/08984e79-a748-4117-bb8d-0684a3fdb068)  

## Future Iterations  
Here are ideas for improvement on future iterations
  - add multithreading so that it does not show Not Responding while scanning or deleting files
  - add a progress bar for scan and delete
  - allow for more granular deletes, pick keep or delete for each instance
  - add better logic for determining original file, doesn't contain -copy, _1, (1)
  - add functionality for moving duplicate files to a new location so they can be sorter through instead of deleting

