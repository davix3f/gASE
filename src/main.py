import gi
import re
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

lines = []
datas = []


with open("/etc/apt/sources.list", "r") as srcs_file:
    for line in srcs_file:
        if line is not "" or "\n":
            lines.append(line)


def get_reponame(line):
    try:
        commented = re.search(r"$#", line)
        http_s = re.search(r"(http|https)://", line)
        domain = re.search(r"(?<=://.+)(\s)", line)
        release_branch = re.search(r")
        free, 
        contrib, 
        free

    except:
        return(False)
    if free is "":
        free_state = True
    else:
        free_state = False
    return(commented, http_s, domain, release_branch, free, contrib, free_state)
    #


for key, value in enumerate(lines):
    if get_reponame(value) is not False:
        print("[-#-match-#-]", value)
        datas.add(get_reponame(value))
    else:
        print("[-!-line got false-!-]", value)

class CRenderTxt(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="APT sources file")

        self.set_default_size(400, 400)

        self.liststore = Gtk.ListStore(str, str)
        for item in datas:
            self.liststore([ ])


        treeview = Gtk.TreeView(model=self.liststore)
        renderer_text = Gtk.CellRendererText()
        column_http_s = Gtk.TreeViewColumn("HyTxProtocol", renderer_text, text=0)
        treeview.append_column(column_http_s)  #

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_domain = Gtk.TreeViewColumn("Domain", renderer_editabletext, text=1)
        treeview.append_column(column_domain)  #

        column_rbranch = Gtk.TreeViewColumn("Branch", renderer_editabletext, text=1)
        treeview.append_column(column_rbranch)  #

        column_free = Gtk.TreeViewColumn("Free-ness", renderer_text, text=0)
        treeview.append_column(column_free) #

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text


win = CRenderTxt()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()



