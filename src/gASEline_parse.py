import re

#"(?P<URL>((?<=(://))?(\S*)))"\
basic_elements = r"(?P<comment>^#(\s*))?"\
              "(?P<binary_src>(deb|deb-src){1})(\s+)"\
              "(?P<URL>((http://|https://)?(\S*)))"\


def line_parse(line):

    strippable_line = line
    branch = ""

    if type(line) is not str:
        raise TypeError("argument not <str>")
    try:
        comment, binary_src, URL = re.search(basic_elements, line).group("comment", "binary_src", "URL")
    except:
        return False

    if comment is None:  # commented T/F
        commented = False
    else:
        commented = True
        strippable_line = strippable_line.replace("#", "")

    if re.search(r"non-free", line):  # free T/F
        free = False
        strippable_line = strippable_line.replace("non-free", "")
    else:
        free = True

    if re.search(r"(\s+)main(\s+)", line):  # main T/F
        main = True
        strippable_line = strippable_line.replace("main", "")
    else:
        main = False

    if re.search(r"contrib", line):  # contrib T/F
        contrib = True
        strippable_line = strippable_line.replace("contrib", "")
    else:
        contrib = False

    if binary_src == "deb-src":  # binary T/F
        binary = False

    if binary_src == "deb":
        binary = True
    
    strippable_line = strippable_line.replace(str(URL), "")
    strippable_line = strippable_line.replace(str(binary_src), "")

    if re.search(r"cdrom:", line):
        #URL = re.search(r"(?<=(cdrom:)).*]/?", line).group()
        URL = re.search(r"cdrom:.*]/?", line).group()

    strippable_line = list(filter(lambda w: w != '', strippable_line.split(" ")))
    
    for item in strippable_line:
        branch += item + " " if strippable_line.index(item) <= len(strippable_line)  else ""

    return(commented, binary, str(URL), str(branch), main, contrib, free, line.rstrip())
