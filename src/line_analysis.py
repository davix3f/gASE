import re


basic_elements = r"(?P<comment>^#(\s+))?"\
              "(?P<binary_src>(deb|deb-src){1})(\s+)"\
              "(?P<http_s>(http://|https://))"\
              "(?P<URL>(?<=(://))(\S*))"\
              "\s+"\
              "(?P<branch>(\S+))"\


def line_parse(line):
    if type(line) is not str:
        raise TypeError("argument not <str>")
    try:
        comment, binary_src, https, URL, branch = re.search(basic_elements, line).group("comment", "binary_src", "http_s", "URL", "branch")
    except:
        return False

    if comment is None:  # commented T/F
        commented = False
    else:
        commented = True
    if re.search(r"non-free", line):  # free T/F
        free = False
    else:
        free = True
    if re.search(r"(\s+)main(\s+)", line):  # main T/F
        main = True
    else:
        main = False
    if re.search(r"contrib", line):  # contrib T/F
        contrib = True
    else:
        contrib = False
    if re.search(r"ftp", line):  # ftp T/F
        ftp = True
    else:
        ftp = False
    if binary_src == "deb-src":  # binary T/F
        binary = False
    if binary_src == "deb":
        binary = True
    if "https" in https:
        https = True
    else:
        https = False

    return(commented, binary, https, URL, branch, main, contrib, free, ftp)
