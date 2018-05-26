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

        treeview = Gtk.TreeView(model=self.liststore)

        rndr_text = Gtk.CellRendererText()  # render text [not editable]

        rndr_URL = Gtk.CellRendererText()  # editable text render URL
        rndr_URL.set_property("editable", True)
        rndr_URL.connect("edited", self.URL_edited)

        rndr_BRANCH = Gtk.CellRendererText()  # editable text render BRANCH
        rndr_BRANCH.set_property("editable", True)
        rndr_BRANCH.connect("edited", self.BRANCH_edited)

        rndr_toggle = Gtk.CellRendererToggle()
        rndr_toggle.connect("toggled", self.on_cell_toggled)


        columns = [
            Gtk.TreeViewColumn("Commented", rndr_toggle, active=0),  # BOOL comment state
            Gtk.TreeViewColumn("Binary", rndr_toggle, active=1),  # BOOL binary/src repo
            Gtk.TreeViewColumn("HTTPS", rndr_toggle, active=2),  # BOOL http/https protocol
            Gtk.TreeViewColumn("URL", rndr_URL, text=3),  # STR url
            Gtk.TreeViewColumn("Branch", rndr_BRANCH, text=4),  # STR release branch (jessie, stable, testing..)
            Gtk.TreeViewColumn("Main", rndr_toggle, active=5),  # BOOL main/not main
            Gtk.TreeViewColumn("Contrib", rndr_toggle, active=6),  # BOOL contrib/not contrib
            Gtk.TreeViewColumn("Free", rndr_toggle, active=7),  # BOOL free/non-free
            Gtk.TreeViewColumn("FTP", rndr_toggle, active=8),  # BOOl ftp/not ftp in URL
            Gtk.TreeViewColumn("Line", rndr_text, text=9)  # STR full line
        ]

        for item in columns:
            treeview.append_column(item)

        self.add(treeview)

        print(treeview.widget)

    def URL_edited(self, widget, path, URL):
        self.liststore[path][3] = URL
    def BRANCH_edited(self, widget, path, BRANCH):
        self.liststore[path][4] = BRANCH

    def on_cell_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]


win = CellRenderWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
