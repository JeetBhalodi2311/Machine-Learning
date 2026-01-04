# Lab 2: Demonstration of Unix Commands

## Part A
**1. Perform the following Unix Commands: who, whoami, uname, passwd, mkdir, rmdir, cp, mv, rm, cut, paste, more**

*   `who`: Displays who is logged on.
*   `whoami`: Displays the effective username of the current user.
*   `uname`: Displays system information (kernel name). `uname -a` gives all info.
*   `passwd`: Used to change the user's password. (Note: Interactive command).
*   `mkdir directory_name`: Creates a new directory.
*   `rmdir directory_name`: Removes an empty directory.
*   `cp source_file destination_file`: Copies a file.
*   `mv old_name new_name`: Moves or renames a file.
*   `rm file_name`: Removes a file.
*   `cut`: Removes sections from each line of files.
*   `paste`: Merges lines of files.
*   `more file_name`: View file content one screen at a time.

---

## Part B

**1. Copy a file file.txt to a new location backup/file.txt, then move it to diet/file.txt**

```bash
mkdir -p backup diet
cp file.txt backup/file.txt
mv backup/file.txt diet/file.txt
```

**2. Extract the first and second fields from a file data.txt and merge them with another file extra.txt column-wise.**

Assuming fields are separated by tabs (default for cut/paste) or spaces. If comma-separated, use `-d ','`.

```bash
cut -f 1,2 data.txt > temp_cut.txt
paste temp_cut.txt extra.txt
rm temp_cut.txt
# Or in one line:
paste <(cut -f 1,2 data.txt) extra.txt
```

**3. Create a directory called backup and copy all .txt files from the current directory into this backup folder.**

```bash
mkdir -p backup
cp *.txt backup/
```

**4. Extract the first three fields from data1.txt, extract the first three fields from data2.txt, and combine them side by side.**

```bash
cut -f 1-3 data1.txt > temp1.txt
cut -f 1-3 data2.txt > temp2.txt
paste temp1.txt temp2.txt
rm temp1.txt temp2.txt
# Or in one line:
paste <(cut -f 1-3 data1.txt) <(cut -f 1-3 data2.txt)
```

---

## Part C

**1. Display the system's kernel version and save the output to a file called sysinfo.txt, then copy the file to a folder named system_backup.**

```bash
uname -r > sysinfo.txt
mkdir -p system_backup
cp sysinfo.txt system_backup/
```

**2. Create a directory project_backup, move all .sh files from the current directory to this new directory, then delete one of the .sh files from the backup.**

```bash
mkdir -p project_backup
mv *.sh project_backup/
# Assuming we want to delete a file named 'script.sh' inside project_backup
# Be careful running this if you don't have .sh files you want to move!
rm project_backup/script.sh
```

**3. Extract specific fields from file1.txt and file2.txt, combine them using paste, and display the result page by page using more.**

Example: Extract field 1 from file1 and field 2 from file2.

```bash
paste <(cut -f 1 file1.txt) <(cut -f 2 file2.txt) | more
```
