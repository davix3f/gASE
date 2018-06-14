import gASEline_parse

class Repo:
    def __init__(self, commented, binary, URL, branch, main, contrib, free, ftp, line, linenum=None):
        self.commented = commented
        self.binary = binary
        self.URL = URL
        self.branch = branch
        self.main = main
        self.contrib = contrib
        self.free = free
        self.ftp = ftp
        self.line = line
        self.linenum = linenum
    edited = ""

    def returnFullInfo(self):
        return(self.commented, self.binary, self.URL,\
               self.branch,self.main, self.contrib, self.free,\
               self.ftp, self.line, self.linenum)

    def buildEdited(self):
        elements = ["#" if self.commented is True else "",
                    "deb" if self.binary is True else "deb-src",
                    self.URL,
                    self.branch,
                    "main" if self.main is True else "",
                    "non-free" if self.free is False else "",
                    "contrib" if self.contrib is True else ""]

        self.edited = ""
        for key, value in enumerate(elements):
            if value != "":
                self.edited += value
                if key != len(elements)-1:
                    self.edited += " "
        print(self.edited)


    def editCommented(self, replacement):
        if self.commented is not replacement:
            self.commented = replacement
            self.buildEdited()

    def editBinary(self, replacement):
        if self.binary is not replacement:
            self.binary = replacement
            self.buildEdited()

    def editURL(self, replacement):
        if self.URL is not replacement:
            self.URL = replacement
            self.buildEdited()

    def editBranch(self, replacement):
        if self.branch is not replacement:
            self.branch = replacement
            self.buildEdited()

    def editMain(self, replacement):
        if self.main is not replacement:
            self.main = replacement
            self.buildEdited()

    def editContrib(self, replacement):
        if self.contrib is not replacement:
            self.contrib = replacement
            self.buildEdited()

    def editFree(self, replacement):
        if self.free is not replacement:
            self.free = replacement
            self.buildEdited()

    @classmethod
    def widget_builder(cls, commented, binary, main, free, contrib, URL, BRANCH):
        final_line = ""
        elements = ["#" if commented is True else "",
                    "deb" if binary is True else "deb-src",
                    URL,
                    BRANCH,
                    "main" if main is True else "",
                    "non-free" if free is False else "",
                    "contrib" if contrib is True else ""]
        for item in elements:
            if item != "":
                if elements.index(item) != len(elements)-1:
                    final_line += (item+" ")
                else:
                    final_line += item
        print(final_line)
        return(cls(*gASEline_parse.line_parse(final_line), None))
