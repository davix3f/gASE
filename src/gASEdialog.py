import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gASEutils


class GeneralDialog(Gtk.Dialog):
    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self, "Message", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.message = message

        box = self.get_content_area().add(Gtk.Label(self.message))

        self.set_default_size(80, 80)
        self.show_all()



class AddRepoDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.commented = False
        self.binary = False
        self.main = False
        self.free = False
        self.contrib = False
        self.URL = None
        self.BRANCH = None

        self.set_default_size(200, 200)
        box = self.get_content_area()

        entry_URL = Gtk.Entry()
        entry_URL.set_placeholder_text("URL")
        entry_URL.connect("activate", self.urledit)

        entry_BRANCH = Gtk.Entry()
        entry_BRANCH.set_placeholder_text("Branch (es \"stretch\")")
        entry_BRANCH.connect("activate", self.branchedit)


        toggles = {
            "commented":Gtk.CheckButton(label="#"),
            "src_bin":Gtk.CheckButton(label="Binary"),
            "main":Gtk.CheckButton(label="Main"),
            "free":Gtk.CheckButton(label="Free"),
            "contrib":Gtk.CheckButton(label="Contrib"),
        }

        functions = {
            "commented":("toggled", self.comment_toggled),
            "src_bin":("toggled", self.binsrc),
            "main":("toggled", self.main_toggled),
            "free":("toggled", self.free_toggled),
            "contrib":("toggled", self.contrib_toggled)
        }

        gASEutils.connect_toggles([*toggles], toggles, functions)
        box.add(Gtk.Label("In text fields, press Enter to confirm"))
        box.add(toggles["commented"])
        box.add(toggles["src_bin"])
        box.add(toggles["main"])
        box.add(toggles["free"])
        box.add(toggles["contrib"])
        box.add(entry_URL)
        box.add(entry_BRANCH)

        self.show_all()


    def comment_toggled(self, widget):
        self.commented = widget.get_active()
        print("Comment", self.commented)

    def binsrc(self, widget):
        self.binary = widget.get_active()
        print("Binary", widget.get_active())

    def main_toggled(self, widget):
        self.main = widget.get_active()
        print("main", widget.get_active())

    def free_toggled(self, widget):
        self.free = widget.get_active()
        print("free", widget.get_active())

    def contrib_toggled(self, widget):
        self.contrib = widget.get_active()
        print("contrib", widget.get_active())

    def urledit(self, widget):
        self.URL = widget.get_text()
        print(self.URL)

    def branchedit(self, widget):
        self.BRANCH = widget.get_text()
        print(self.BRANCH)

    def build(self):
        if (self.URL != None) and (self.BRANCH != None):
            print("New repo:\nCommented:",self.commented,"\nBinary:",self.binary,\
                  "\nMain:",self.main,"\nFree:",self.free,"\nContrib:",self.contrib,\
                  "\nURL:",self.URL,"\nBranch:",self.BRANCH)
            return(self.commented, self.binary, self.main, self.free, self.contrib, self.URL, self.BRANCH)
        else:
            emptiness_dialog = GeneralDialog(self, "URL/BRANCH is empty!")
            emptiness_response = emptiness_dialog.run()
            if emptiness_response:
                emptiness_dialog.hide()
