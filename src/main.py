import gi
import re

import line_analysis
line_parse = line_analysis.line_parse

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

lines = []
datas = []


with open("/etc/apt/sources.list", "r") as srcs_file:
    for line in srcs_file:
        if line is not "" or "\n":
            lines.append(line)

for item in lines:
    if line_parse(item) != False:
        datas.append(line_parse(item))



class CellRenderWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="APT sources editor")

        self.set_default_size(400, 400)

        self.liststore = Gtk.ListStore(bool, bool, bool, str, str, bool, bool, bool, bool, str)
        for item in datas:
            self.liststore.append([*item])

        for k, v in enumerate(self.liststore):
            print(k, v)
            for key, value in enumerate(item):
                print(key, value)
            print()

        treeview = Gtk.TreeView(model=self.liststore)

        rndr_text = Gtk.CellRendererText()  # renderer text [not editable]

        rndr_URL = Gtk.CellRendererText()  # editable text renderer URL
        rndr_URL.set_property("editable", True)
        rndr_URL.connect("edited", self.URL_edited)

        rndr_BRANCH = Gtk.CellRendererText()  # editable text renderer BRANCH
        rndr_BRANCH.set_property("editable", True)
        rndr_BRANCH.connect("edited", self.BRANCH_edited)

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
            Gtk.TreeViewColumn("Line", rndr_text, text=9)  # STR full line
        ]

        for item in columns:
            treeview.append_column(item)

        self.add(treeview)


    def URL_edited(self, widget, path, URL):
        self.liststore[path][3] = URL

    def BRANCH_edited(self, widget, path, BRANCH):
        self.liststore[path][4] = BRANCH

    def comment_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]
        print("Comment is now", widget.get_active())

    def binary_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]
        print("Binary is now", widget.get_active())

    def HTTPS_toggled(self, widget, path):
        self.liststore[path][2] = not self.liststore[path][2]
        print("HTTPS is now", widget.get_active())

    def main_toggled(self, widget, path):
        self.liststore[path][5] = not self.liststore[path][5]
        print("Main is now", widget.get_active())

    def contrib_toggled(self, widget, path):
        self.liststore[path][6] = not self.liststore[path][6]
        print("Contrib is now", widget.get_active())

    def free_toggled(self, widget, path):
        self.liststore[path][7] = not self.liststore[path][7]
        print("Free is now", widget.get_active())


win = CellRenderWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
