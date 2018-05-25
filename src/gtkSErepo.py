class Repo:
    def __init__(self, commented, binary, https, URL, branch, main, contrib, free, ftp):
        self.commented = commented
        self.binary = binary
        self.https = https
        self.URL = URL
        self.branch = branch
        self.main = main
        self.free = free
        self.ftp = ftp

    def returnFullInfo(self):
        return(commented, binary, https, URL, branch, main, free, ftp)
