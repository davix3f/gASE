from shutil import copyfile
from os import getcwd

def rewrite(lines, to_replace, file, backup=True):
    any_edit = False
    if backup is True:
        copyfile(file, file+".bkp")
        print("File \'{0}\' has been backed up as \'{1}\'".format(file, file+"bkp"))


    for key, value in enumerate(lines):
        for item in to_replace:
            if item.linenum == key:
                if (item.edited != "") and (item.edited != item.line):
                    any_edit = True
                    print("lines[{0}] found modified from {1} to {2}".format(key, lines[key], item.edited))
                    oldval = lines[key]
                    lines[key] = item.edited
                    print("{0} has been replaced with \'{1}\'".format(oldval, lines[key]))
                to_replace.remove(item)
    if len(to_replace) > 0:
        for item in to_replace:
            if (item.edited != "") and (item.edited != item.line):
                lines.append(item.edited)
            else:
                lines.append(item.line)
    if any_edit is False:
        print("Any edit found")
        return(False)
    else:
        with open(file, "w") as file:
            for item in lines:
                file.write(item)
