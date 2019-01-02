import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import re
from os import path
import sys

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

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

        self.set_default_size(900, 500)
        self.connect("delete-event", Gtk.main_quit)

        self.liststore = Gtk.ListStore(bool,  # commented 0
                                       bool,  # binary 1
                                       str,  # url 2
                                       str,  # branch 3
                                       bool,  # main 4
                                       bool,  # contrib 5
                                       bool,  # free 6
                                       str,  # line 7
                                       int,  # line n 8
                                       str # edited line preview 9
                                       )
        [self.commented_index,
         self.binary_index,
         self.url_index,
         self.branch_index,
         self.main_index,
         self.contrib_index,
         self.free_index,
         self.line_index,
         self.linen_index,
         self.edited_index] = list(range(0, self.liststore.get_n_columns()))

        for item in self.repo_instances:
            self.liststore.append([*item.returnFullInfo(), None])


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
            "write":Gtk.Button("Write edits"),
            #"remove":Gtk.Button("Remove repo"),
            "add_repo":Gtk.Button("Add repo")
        }
        toggles_kw_list = [*toggles]

        toggles_functions = {
            "commented":("toggled", self.comment_toggled),
            "binary":("toggled", self.binary_toggled),
            "main":("toggled", self.main_toggled),
            "contrib":("toggled", self.contrib_toggled),
            "free":("toggled", self.free_toggled),
            "write":("clicked", self.write_new_repos),
            #"remove":("clicked", self.remove_repo),
            "add_repo":("clicked", self.add_repo)
        }

        if gASEutils.connect_toggles(toggles_kw_list, toggles, toggles_functions) is False:
            quit()

        columns = [
            # BOOLS
            Gtk.TreeViewColumn("Commented", toggles["commented"], active=self.commented_index),  # BOOL '^#' state
            Gtk.TreeViewColumn("Binary", toggles["binary"], active=self.binary_index),  # BOOL binary/src repo
            Gtk.TreeViewColumn("Main", toggles["main"], active=self.main_index),  # BOOL main/not main
            Gtk.TreeViewColumn("Contrib", toggles["contrib"], active=self.contrib_index),  # BOOL contrib/not contrib
            Gtk.TreeViewColumn("Free", toggles["free"], active=self.free_index),  # BOOL free/non-free
            # STRINGS
            Gtk.TreeViewColumn("URL", rndr_URL, text=self.url_index),  # STR url
            Gtk.TreeViewColumn("Branch", rndr_BRANCH, text=self.branch_index),  # STR release branch (jessie, stable, testing..)
            #Gtk.TreeViewColumn("Line", rndr_text, text=self.line_index),  # STR full line
            Gtk.TreeViewColumn("Line#", rndr_text, text=self.linen_index),  # STR(int) LINE#
            Gtk.TreeViewColumn("Edit result", rndr_edit_preview, text=self.edited_index)  # STR line edit result
        ]


        for item in columns:
            treeview.append_column(item)

        scrolledwin = Gtk.ScrolledWindow()
        scrolledwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolledwin.add(treeview)
        scrolledwin.set_min_content_height(200)

        obox.pack_start(toggles["write"], False, False, 0)
        #obox.pack_start(toggles["remove"], False, False, 1)
        obox.pack_start(toggles["add_repo"], False, False, 1)

        vbox.pack_start(obox, False, False, 0)
        vbox.pack_start(scrolledwin, True, True, 0)

        self.add(vbox)


    def editpreview(self, path):
        if self.repo_instances[int(path)].edited != self.repo_instances[int(path)].line:
            self.liststore[path][self.edited_index] = self.repo_instances[int(path)].edited

    def URL_edited(self, widget, path, URL):
        oldURL = self.liststore[path][self.url_index]
        self.liststore[path][self.url_index] = URL
        self.repo_instances[int(path)].editURL(URL)
        print("\'" + oldURL + "\' changed to \'" + URL + "\'")
        self.editpreview(path)

    def BRANCH_edited(self, widget, path, BRANCH):
        self.liststore[path][self.branch_index] = BRANCH
        self.repo_instances[int(path)].editBranch(BRANCH)
        self.editpreview(path)

    def comment_toggled(self, widget, path):
        self.liststore[path][self.commented_index] = not self.liststore[path][self.commented_index]
        self.repo_instances[int(path)].editCommented(self.liststore[path][self.commented_index])
        print("Comment is now", self.liststore[path][self.commented_index])
        self.editpreview(path)

    def binary_toggled(self, widget, path):
        self.liststore[path][self.binary_index] = not self.liststore[path][self.binary_index]
        self.repo_instances[int(path)].editBinary(self.liststore[path][self.binary_index])
        print("Binary is now", self.liststore[path][self.binary_index])
        self.editpreview(path)

    def main_toggled(self, widget, path):
        self.liststore[path][self.main_index] = not self.liststore[path][self.main_index]
        self.repo_instances[int(path)].editMain(self.liststore[path][self.main_index])
        print("Main is now", self.liststore[path][self.main_index])
        self.editpreview(path)

    def contrib_toggled(self, widget, path):
        self.liststore[path][self.contrib_index] = not self.liststore[path][self.contrib_index]
        self.repo_instances[int(path)].editContrib(self.liststore[path][self.contrib_index])
        print("Contrib is now", self.liststore[path][self.contrib_index])
        self.editpreview(path)

    def free_toggled(self, widget, path):
        print(self)
        print(path)
        self.liststore[path][self.free_index] = not self.liststore[path][self.free_index]
        self.repo_instances[int(path)].editFree(self.liststore[path][self.free_index])
        print("Free is now", self.liststore[path][self.free_index])
        self.editpreview(path)

    def write_new_repos(self, widget):
        if self.show_dialog("Write edits?") is True:
            gASE_rewrite.rewrite(self.lines, self.repo_instances, "/etc/apt/sources.list")

    def remove_repo(self, widget):
        print(self.liststore.get_selection())
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
        active_dialog = gASEdialog.GeneralDialog(self, message)
        dialog_response = active_dialog.run()

        if dialog_response == Gtk.ResponseType.OK:
            print("Ok")
            active_dialog.destroy()
            return(True)
        elif dialog_response == Gtk.ResponseType.CANCEL:
            print("Cancelled")
            active_dialog.destroy()
            return(False)
