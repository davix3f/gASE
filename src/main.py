import gi
import re

import line_analysis
from gASErepo import Repo
line_parse = line_analysis.line_parse

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

lines = []
datas = []
repo_instances = []

with open("/etc/apt/sources.list", "r") as srcs_file:
    for line in srcs_file:
        lines.append(line)
print(len(lines))

for key, value in enumerate(lines):
    if line_parse(value) != False:
        datas.append(line_parse(value))
        repo_instances.append(Repo(*line_parse(value), key))



class CellRenderWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="APT sources editor")

        self.set_default_size(800, 500)

        self.liststore = Gtk.ListStore(bool,  # commented 0
                                       bool,  # binary 1
                                       bool,  # https 2
                                       str,  # url 3
                                       str,  # branch 4
                                       bool,  # main 5
                                       bool,  # free 6
                                       bool,  # contrib 7
                                       bool,  # ftp 8
                                       str,  # line 9
                                       int,  # line n 10
                                       str # edited line preview 11
                                       )
        for item in repo_instances:
            self.liststore.append([*item.returnFullInfo(), "Not edited"])


        treeview = Gtk.TreeView(model=self.liststore)

        rndr_text = Gtk.CellRendererText()  # renderer text [not drectly editable]

        rndr_URL = Gtk.CellRendererText()  # editable text renderer URL
        rndr_URL.set_property("editable", True)
        rndr_URL.connect("edited", self.URL_edited)

        rndr_BRANCH = Gtk.CellRendererText()  # editable text renderer BRANCH
        rndr_BRANCH.set_property("editable", True)
        rndr_BRANCH.connect("edited", self.BRANCH_edited)

        rndr_edit_preview = Gtk.CellRendererText()

        toggles = {
            "commented":Gtk.CellRendererToggle(),
            "binary":Gtk.CellRendererToggle(),
            "HTTPS":Gtk.CellRendererToggle(),
            "main":Gtk.CellRendererToggle(),
            "contrib":Gtk.CellRendererToggle(),
            "free":Gtk.CellRendererToggle(),
            "ftp":Gtk.CellRendererToggle()
        }
        toggles_kw_list = [*toggles]

        def list_epure(target_list, *args):
            for item in args:
                target_list.remove(item)
                print("Removed \'%s\'" % item)

        list_epure(toggles_kw_list, "ftp")

        toggles_functions = {
            "commented":("toggled", self.comment_toggled),
            "binary":("toggled", self.binary_toggled),
            "HTTPS":("toggled", self.HTTPS_toggled),
            "main":("toggled", self.main_toggled),
            "contrib":("toggled", self.contrib_toggled),
            "free":("toggled", self.free_toggled)
        }

        def connect_toggles(toggles_list, toggles_dictionary, functions_dictionary):
            if len(toggles_list) != len(functions_dictionary):
                print("The length of the argument \'toggles_list\' is", len(toggles_list),\
                      "while the length of the \'functions_dictionary\' argument is", len(functions_dictionary))
                return(False)
            index = 0
            while index < len(toggles_list):
                print(toggles_dictionary[toggles_list[index]], functions_dictionary[toggles_list[index]])
                toggles_dictionary[toggles_list[index]].connect(functions_dictionary[toggles_list[index]][0],\
                                                                functions_dictionary[toggles_list[index]][1])
                index += 1

        if connect_toggles(toggles_kw_list, toggles, toggles_functions) is False:
            quit()

        columns = [
            # BOOLS
            Gtk.TreeViewColumn("Commented", toggles["commented"], active=0),  # BOOL '^#' state
            Gtk.TreeViewColumn("Binary", toggles["binary"], active=1),  # BOOL binary/src repo
            Gtk.TreeViewColumn("HTTPS", toggles["HTTPS"], active=2),  # BOOL http/https protocol
            Gtk.TreeViewColumn("Main", toggles["main"], active=5),  # BOOL main/not main
            Gtk.TreeViewColumn("Contrib", toggles["contrib"], active=6),  # BOOL contrib/not contrib
            Gtk.TreeViewColumn("Free", toggles["free"], active=7),  # BOOL free/non-free
            Gtk.TreeViewColumn("FTP", toggles["ftp"], active=8),  # BOOl ftp/not ftp in URL
            # STRINGS
            Gtk.TreeViewColumn("URL", rndr_URL, text=3),  # STR url
            Gtk.TreeViewColumn("Branch", rndr_BRANCH, text=4),  # STR release branch (jessie, stable, testing..)
            Gtk.TreeViewColumn("Line", rndr_text, text=9),  # STR full line
            Gtk.TreeViewColumn("Line#", rndr_text, text=10),  # STR(int) LINE#
            Gtk.TreeViewColumn("Edit result", rndr_edit_preview, text=11)  # STR line edit result
        ]


        for item in columns:
            treeview.append_column(item)

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolledwin.add(treeview)
        scrolledwin.set_min_content_height(200)

        self.add(scrolledwin)

    def editpreview(self, path):
        if repo_instances[int(path)].edited != repo_instances[int(path)].line:
            self.liststore[path][11] = repo_instances[int(path)].edited

    def URL_edited(self, widget, path, URL):
        oldURL = self.liststore[path][3]
        self.liststore[path][3] = URL
        repo_instances[int(path)].editURL(URL)
        if re.search(r"(http://|https://)?ftp\.", URL):
            self.liststore[path][8] = True
        else:
            self.liststore[path][8] = False
        print("\'" + oldURL + "\' changed to \'" + URL + "\'")
        self.editpreview(path)


    def BRANCH_edited(self, widget, path, BRANCH):
        self.liststore[path][4] = BRANCH
        repo_instances[int(path)].editBranch(BRANCH)
        self.editpreview(path)


    def comment_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]
        repo_instances[int(path)].editCommented(self.liststore[path][0])
        print("Comment is now", widget.get_active())
        self.editpreview(path)

    def binary_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]
        repo_instances[int(path)].editBinary(self.liststore[path][2])
        print("Binary is now", widget.get_active())
        self.editpreview(path)

    def HTTPS_toggled(self, widget, path):
        self.liststore[path][2] = not self.liststore[path][2]
        repo_instances[int(path)].editHTTPS(self.liststore[path][2])
        print("HTTPS is now", widget.get_active())
        self.editpreview(path)

    def main_toggled(self, widget, path):
        self.liststore[path][5] = not self.liststore[path][5]
        repo_instances[int(path)].editMain(self.liststore[path][5])
        print("Main is now", widget.get_active())
        self.editpreview(path)

    def contrib_toggled(self, widget, path):
        self.liststore[path][6] = not self.liststore[path][6]
        repo_instances[int(path)].editContrib(self.liststore[path][6])
        print("Contrib is now", widget.get_active())
        self.editpreview(path)

    def free_toggled(self, widget, path):
        self.liststore[path][7] = not self.liststore[path][7]
        repo_instances[int(path)].editFree(self.liststore[path][7])
        print("Free is now", widget.get_active())
        self.editpreview(path)


win = CellRenderWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
