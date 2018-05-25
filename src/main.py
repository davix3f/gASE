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

        self.liststore = Gtk.ListStore(bool, bool, bool, str, str, bool, bool, bool, bool)
        for item in datas:
            self.liststore.append([*item])

        treeview = Gtk.TreeView(model=self.liststore)

        rndr_text = Gtk.CellRendererText()  # render text

        rndr_editabletext = Gtk.CellRendererText()  # editable text renderer
        rndr_editabletext.set_property("editable", True)

        rndr_toggle = Gtk.CellRendererToggle()
        rndr_toggle.connect("toggled", self.on_cell_toggled)

# BOOL comment state
        column_comment = Gtk.TreeViewColumn("Commented", rndr_toggle, active=1)
        treeview.append_column(column_comment)
# BOOL binary/src repo
        column_binary = Gtk.TreeViewColumn("Binary", rndr_toggle, active=1)
        treeview.append_column(column_binary)
# BOOL http/https protocol
        column_https = Gtk.TreeViewColumn("HTTP", rndr_toggle, active=1)
        treeview.append_column(column_https)
# STR url
        column_domain = Gtk.TreeViewColumn("URL", rndr_editabletext, text=1)
        treeview.append_column(column_domain)
# STR release branch (jessie, stable, testing..)
        column_branch = Gtk.TreeViewColumn("Branch", rndr_editabletext, text=1)
        treeview.append_column(column_branch)
# BOOL main/not main
        column_main = Gtk.TreeViewColumn("Main", rndr_toggle, active=1)
        treeview.append_column(column_main)
# BOOL contrib/not contrib
        column_contrib = Gtk.TreeViewColumn("Contrib", rndr_toggle, active=1)
        treeview.append_column(column_contrib)
# BOOL free/non-free
        column_free = Gtk.TreeViewColumn("Free", rndr_toggle, active=1)
        treeview.append_column(column_free)
# BOOl ftp/not ftp in URL
        column_ftp = Gtk. TreeViewColumn("FTP", rndr_toggle, active=0)

        rndr_editabletext.connect("edited", self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def on_cell_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]


win = CellRenderWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
