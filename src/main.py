import re
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# custom modules
import line_analysis
from gASErepo import Repo
from gASE_main_window import MainWindow
line_parse = line_analysis.line_parse


lines = []
datas = []
repo_instances = []

with open("/etc/apt/sources.list", "r") as srcs_file:
    for line in srcs_file:
        lines.append(line if line == "\n" else line.rstrip())

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
