import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GeneralDialog(Gtk.Dialog):
    def __init__(self, parent, alert):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK))
        if type(alert) == str:
            self.alert = alert
        else:
            raise TypeError("\'Alert\' must be string")

        box = self.get_content_area().add(Gtk.Label(self.alert))

        self.set_default_size(80, 80)
        self.show_all()
