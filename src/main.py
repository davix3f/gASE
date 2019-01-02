import re
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from os import path
import sys

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))

# custom modules
import gASEline_parse
from gASErepo import Repo
from gASE_main_window import MainWindow
line_parse = gASEline_parse.line_parse


lines = []
datas = []
repo_instances = []

with open("/etc/apt/sources.list", "r") as srcs_file:
    for line in srcs_file:
        if line != "\n":
                lines.append(line.rstrip())


for key, value in enumerate(lines):
    if line_parse(value) != False:
        datas.append(line_parse(value))
        repo_instances.append(Repo(*line_parse(value), key))


MainWindow(lines, datas, repo_instances).show_all()
print("Starting main window using Gtk",\
      str(Gtk.get_major_version()) +"."+\
      str(Gtk.get_minor_version()) +"."+\
      str(Gtk.get_micro_version()))
Gtk.main()
