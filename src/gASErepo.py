class Repo:
    def __init__(self, commented, binary, https, URL, branch, main, contrib, free, ftp, line, linenum):
        self.commented = commented
        self.binary = binary
        self.https = https
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
        return(self.commented, self.binary, self.https, self.URL,\
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

    def editHTTPS(self, replacement):
        if self.https is not replacement:
            self.https = replacement
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
