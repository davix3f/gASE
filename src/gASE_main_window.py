import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import re

import gASE_rewrite
import gASEdialog
import gASEutils
import gASErepo

class MainWindow(Gtk.Window):

    def __init__(self, lines, datas, repo_instances):
        Gtk.Window.__init__(self, title="APT sources editor")

        self.lines = lines
        self.datas = datas
        self.repo_instances = repo_instances

        self.set_default_size(800, 500)
        self.connect("delete-event", Gtk.main_quit)

        self.liststore = Gtk.ListStore(bool,  # commented 0
                                       bool,  # binary 1
                                       str,  # url 2
                                       str,  # branch 3
                                       bool,  # main 4
                                       bool,  # free 5
                                       bool,  # contrib 6
                                       bool,  # ftp 7
                                       str,  # line 8
                                       int,  # line n 9
                                       str # edited line preview 10
                                       )
        for item in self.repo_instances:
            self.liststore.append([*item.returnFullInfo(), "Not edited"])


        treeview = Gtk.TreeView(model=self.liststore)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        obox = Gtk.Box()

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
            "main":Gtk.CellRendererToggle(),
            "contrib":Gtk.CellRendererToggle(),
            "free":Gtk.CellRendererToggle(),
            "ftp":Gtk.CellRendererToggle(),
            "write":Gtk.Button("Write modifies"),
            "remove":Gtk.Button("Remove repo"),
            "add_repo":Gtk.Button("Add repo")
        }
        toggles_kw_list = [*toggles]

        gASEutils.list_epure(toggles_kw_list, "ftp")

        toggles_functions = {
            "commented":("toggled", self.comment_toggled),
            "binary":("toggled", self.binary_toggled),
            "main":("toggled", self.main_toggled),
            "contrib":("toggled", self.contrib_toggled),
            "free":("toggled", self.free_toggled),
            "write":("clicked", self.write_new_repos),
            "remove":("clicked", self.remove_repo),
            "add_repo":("clicked", self.add_repo)
        }



        if gASEutils.connect_toggles(toggles_kw_list, toggles, toggles_functions) is False:
            quit()

        columns = [
            # BOOLS
            Gtk.TreeViewColumn("Commented", toggles["commented"], active=0),  # BOOL '^#' state
            Gtk.TreeViewColumn("Binary", toggles["binary"], active=1),  # BOOL binary/src repo
            Gtk.TreeViewColumn("Main", toggles["main"], active=4),  # BOOL main/not main
            Gtk.TreeViewColumn("Contrib", toggles["contrib"], active=5),  # BOOL contrib/not contrib
            Gtk.TreeViewColumn("Free", toggles["free"], active=6),  # BOOL free/non-free
            Gtk.TreeViewColumn("FTP", toggles["ftp"], active=7),  # BOOl ftp/not ftp in URL
            # STRINGS
            Gtk.TreeViewColumn("URL", rndr_URL, text=2),  # STR url
            Gtk.TreeViewColumn("Branch", rndr_BRANCH, text=3),  # STR release branch (jessie, stable, testing..)
            Gtk.TreeViewColumn("Line", rndr_text, text=8),  # STR full line
            Gtk.TreeViewColumn("Line#", rndr_text, text=9),  # STR(int) LINE#
            Gtk.TreeViewColumn("Edit result", rndr_edit_preview, text=10)  # STR line edit result
        ]


        for item in columns:
            treeview.append_column(item)

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolledwin.add(treeview)
        scrolledwin.set_min_content_height(200)

        obox.pack_start(toggles["write"], False, False, 0)
        obox.pack_start(toggles["remove"], False, False, 1)
        obox.pack_start(toggles["add_repo"], False, False, 1)

        vbox.pack_start(obox, False, False, 0)
        vbox.pack_start(scrolledwin, True, True, 0)

        self.add(vbox)

    def editpreview(self, path):
        if self.repo_instances[int(path)].edited != self.repo_instances[int(path)].line:
            self.liststore[path][11] = self.repo_instances[int(path)].edited

    def URL_edited(self, widget, path, URL):
        oldURL = self.liststore[path][3]
        self.liststore[path][3] = URL
        self.repo_instances[int(path)].editURL(URL)
        if re.search(r"(http://|https://)?ftp\.", URL):
            self.liststore[path][8] = True
        else:
            self.liststore[path][8] = False
        print("\'" + oldURL + "\' changed to \'" + URL + "\'")
        self.editpreview(path)


    def BRANCH_edited(self, widget, path, BRANCH):
        self.liststore[path][4] = BRANCH
        self.repo_instances[int(path)].editBranch(BRANCH)
        self.editpreview(path)


    def comment_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]
        self.repo_instances[int(path)].editCommented(self.liststore[path][0])
        print("Comment is now", self.liststore[path][0])
        self.editpreview(path)

    def binary_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]
        self.repo_instances[int(path)].editBinary(self.liststore[path][2])
        print("Binary is now", self.liststore[path][1])
        self.editpreview(path)

    def HTTPS_toggled(self, widget, path):
        self.liststore[path][2] = not self.liststore[path][2]
        self.repo_instances[int(path)].editHTTPS(self.liststore[path][2])
        print("HTTPS is now", self.liststore[path][2])
        self.editpreview(path)

    def main_toggled(self, widget, path):
        self.liststore[path][5] = not self.liststore[path][5]
        self.repo_instances[int(path)].editMain(self.liststore[path][5])
        print("Main is now", self.liststore[path][5])
        self.editpreview(path)

    def contrib_toggled(self, widget, path):
        self.liststore[path][6] = not self.liststore[path][6]
        self.repo_instances[int(path)].editContrib(self.liststore[path][6])
        print("Contrib is now", self.liststore[path][6])
        self.editpreview(path)

    def free_toggled(self, widget, path):
        self.liststore[path][7] = not self.liststore[path][7]
        self.repo_instances[int(path)].editFree(self.liststore[path][7])
        print("Free is now", self.liststore[path][7])
        self.editpreview(path)

    def write_new_repos(self, widget):
        if self.show_dialog("Write edits?") is True:
            gASE_rewrite.rewrite(self.lines, self.repo_instances, "/etc/apt/sources.list")

    def remove_repo(self, widget):
        print("Repo removed")

    def add_repo(self, widget):
        repo_dialog = gASEdialog.AddRepoDialog(self)
        response = repo_dialog.run()
        if response == Gtk.ResponseType.OK:
            if repo_dialog.build() is not False:
                self.repo_instances.append(gASErepo.Repo.widget_builder(*repo_dialog.build()))
                self.repo_instances[-1].linenum = len(self.lines)
                self.liststore.append([*self.repo_instances[-1].returnFullInfo(), "Not edited"])
                print("Repo added")
                repo_dialog.destroy()
        else:
            repo_dialog.destroy()


    def show_dialog(self, message):
        active_dialog = gASEdialog.GeneralDialog(self, "Message dialog", message)
        dialog_response = active_dialog.run()

        if dialog_response == Gtk.ResponseType.OK:
            print("Ok")
            active_dialog.destroy()
            return(True)
        elif dialog_response == Gtk.ResponseType.CANCEL:
            print("Cancelled")
            active_dialog.destroy()
            return(False)
