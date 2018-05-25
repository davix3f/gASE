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
        print(line_parse(item))
    else:
        print("[-no match for]", item.rstrip())



class CRenderTxt(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="APT sources file")

        self.set_default_size(400, 400)

        self.liststore = Gtk.ListStore(bool, bool, bool, str, str, bool, bool, bool, bool)
        for item in datas:
            self.liststore.append([*item])


        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()  # render text

        renderer_editabletext = Gtk.CellRendererText()  # editable text renderer
        renderer_editabletext.set_property("editable", True)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)


        column_comment = Gtk.TreeViewColumn("Commented", renderer_toggle, active=1)
        treeview.append_column(column_comment)

        column_binary = Gtk.TreeViewColumn("Binary", renderer_toggle, active=1)
        treeview.append_column(column_binary)

        column_https = Gtk.TreeViewColumn("HTTP", renderer_toggle, active=1)
        treeview.append_column(column_https)

        column_domain = Gtk.TreeViewColumn("URL", renderer_editabletext, text=1)
        treeview.append_column(column_domain)

        column_branch = Gtk.TreeViewColumn("Branch", renderer_editabletext, text=1)
        treeview.append_column(column_branch)

        column_main = Gtk.TreeViewColumn("Main", renderer_toggle, active=1)
        treeview.append_column(column_main)

        column_contrib = Gtk.TreeViewColumn("Contrib", renderer_toggle, active=1)
        treeview.append_column(column_contrib)

        column_free = Gtk.TreeViewColumn("Free", renderer_toggle, active=1)
        treeview.append_column(column_free)

        column_ftp = Gtk. TreeViewColumn("FTP", renderer_toggle, active=0)

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def on_cell_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]


win = CRenderTxt()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
