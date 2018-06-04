import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import gASE_rewrite
import gASEdialog

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
            "HTTPS":Gtk.CellRendererToggle(),
            "main":Gtk.CellRendererToggle(),
            "contrib":Gtk.CellRendererToggle(),
            "free":Gtk.CellRendererToggle(),
            "ftp":Gtk.CellRendererToggle(),
            "write":Gtk.Button("Write modifies"),
            "remove":Gtk.Button("Remove repo"),
            "add_repo":Gtk.Button("Add repo")
        }
        toggles_kw_list = [*toggles]

        def list_epure(target_list, *args):
            try:
                for item in args:
                    target_list.remove(item)
                    print("Removed \'%s\'" % item)
                return(True)
            except:
                return(False)

        list_epure(toggles_kw_list, "ftp")

        toggles_functions = {
            "commented":("toggled", self.comment_toggled),
            "binary":("toggled", self.binary_toggled),
            "HTTPS":("toggled", self.HTTPS_toggled),
            "main":("toggled", self.main_toggled),
            "contrib":("toggled", self.contrib_toggled),
            "free":("toggled", self.free_toggled),
            "write":("clicked", self.write_new_repos),
            "remove":("clicked", self.remove_repo),
            "add_repo":("clicked", self.add_repo)
        }

        def connect_toggles(toggles_list, toggles_dictionary, functions_dictionary):
            if len(toggles_list) != len(functions_dictionary):
                print("The length of the argument \'toggles_list\' is", len(toggles_list),\
                      "while the length of the \'functions_dictionary\' argument is", len(functions_dictionary))
                return(False)
            index = 0
            while index < len(toggles_list):
                #print(toggles_dictionary[toggles_list[index]], functions_dictionary[toggles_list[index]])
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
        print("Added repo")

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
