import os
import shutil
import pwd
from datetime import datetime
from pwd import getpwuid

# Simple shell
# COMMANDS          ERRORS CHECKED
# 1. info XX         - check file/dir exists
# 2. files
# 3. delete  XX      - check file exists and delete succeeds
# 4. copy XX YY      - XX exists, YY does not exist copy succeeds
# 5. where
# 6. down DD         - check directory exists and change succeeds
# 7. up              - check not at the top of the directory tree - can't go up from root
# 8. finish

# Print a header.
def print_header(headers, width):
    field_num = 0
    output = ''
    while field_num < len(headers):
        output += '{field:{fill}<{width}}'.format(field=headers[field_num], fill=' ', width=width[field_num])
        field_num += 1

    print output
    length = sum(width)
    print '-' * length

# Print file info
def print_file_info(info, width):
    fieldNum = 0
    output = ''
    while fieldNum < len(info):
        output += '{field:{fill}<{width}}'.format(field=info[fieldNum], fill=' ', width=width[fieldNum])
        fieldNum += 1
    print output

# List files and directories
def files_cmd(fields):
    if not checkArgs(fields, 0): return
    headers = ["Name", "Type"]
    width = [30, 15]
    print_header(headers, width)
    for file in os.listdir('.'):
        info = []
        info.append(file)
        if os.path.isdir(file):
            info.append("dir")
        elif os.path.islink(file):
            info.append("link")
        else:
            info.append("file")
        print_file_info(info, width)


# List file info for a single argument
def info_cmd(fields):
    if not checkArgs(fields, 1): return
    headers = ["Name", "Type", "Owner", "Last Changed", "Size (bytes)", "Executable"]
    width = [20, 15, 20, 30, 15, 15]
    info = []
    file = fields[1]
    if os.path.exists(file):
        info.append(file)
        if os.path.isdir(file):
            info.append("dir")
        elif os.path.islink(file):
            info.append("link")
        else:
            info.append("file")
        info.append(getpwuid(os.stat(file).st_uid).pw_name)
        info.append(datetime.fromtimestamp(os.stat(file).st_mtime).strftime('%b %d %Y %H:%M:%S'))
        if not os.path.isdir(file):
            info.append(os.stat(file).st_size)
            info.append("True" if os.access(file, os.X_OK) else "False")
        else:
            info.append("")
            info.append("")
        print_header(headers, width)
        print_file_info(info, width)
    else:
        print "File or directory does not exist."

# Delete file
def delete_cmd(fields):
    if not checkArgs(fields, 1): return
    file = fields[1]
    if not os.path.exists(file): print "File does not exist so cannot be deleted."; return
    try:
        os.remove(file)
        print "File successfully removed"
    except OSError as error:
        print error
        print "File was not deleted."

# copy file from source to dest
def copy_cmd(fields):
    if not checkArgs(fields, 2): return
    source = fields[1]
    dest = fields[2]
    if not os.path.exists(source): print "Source file does not exist."; return
    if os.path.exists(dest): print "Destination file already exists."; return
    try:
        shutil.copyfile(source, dest)
    except PermissionError:
        print "Permission denied."
    except:
        print "Failed copying file for unknown reason."

# pwd
def where_cmd(fields):
    if not checkArgs(fields, 0): return
    print os.getcwd()


# cd into someDirectory
def down_cmd(fields):
    if not checkArgs(fields, 1): return
    dir = fields[1]
    if os.path.exists(dir) and not os.path.isdir(dir):
        print "File exists but is not a directory - cannot change working directory."; return
    elif not os.path.exists(dir): print "Directory does not exist."; return
    os.chdir(dir)
    print "Success, current directoy: " + os.getcwd()


# cd ..
def up_cmd(fields):
    if not checkArgs(fields, 0): return
    if os.getcwd() == "/":
        print "You are already at the top of the directory tree."
        return
    else:
        os.chdir("..")
        print "Success, current directoy: " + os.getcwd()



# check arguments for a given command
def checkArgs(fields, num):
    numArgs = len(fields) - 1
    if numArgs == num:
        return True
    if numArgs > num:
        print "  Unexpected argument " + "'" + fields[num+1] + "'" + " for command " + fields[0]
    else:
        print "  Missing argument for command " + fields[0]

    return False

# ----------------------------------------------------------------------------------------------------------------------

# Run shell
print "Enter 'finish' to quit."
while True:
    line = raw_input("PShell>")
    fields = line.split()
    # split the command into fields stored in the fields list
    # fields[0] is the command name and anything that follows (if it follows) is an argument to the command

    if len(fields) == 0:
        pass
    elif fields[0] == "finish":
        break
    elif fields[0] == "files":
        files_cmd(fields)
    elif fields[0] == "info":
        info_cmd(fields)
    elif fields[0] == "delete":
        delete_cmd(fields)
    elif fields[0] == "copy":
        copy_cmd(fields)
    elif fields[0] == "where":
        where_cmd(fields)
    elif fields[0] == "down":
        down_cmd(fields)
    elif fields[0] == "up":
        up_cmd(fields)
    else:
        print "Unknown command " + fields[0]
