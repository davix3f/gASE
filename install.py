from os import system as shell
from os import makedirs
from os import listdir
from os import getcwd as pwd
import os.path
from shutil import copyfile, copy
from shutil import copytree as copydir
from getpass import getuser
import re

try:
        cd = os.chdir

        # get root

        if getuser() != "root":
            print("The current user is \'%s\', and seems it's not allowed to write in /opt. Please, run the script as superuser [sudo python3 gase.py]" % getuser())
            exit()

        cd("/tmp")

        # clone repo
        if shell("git clone https://github.com/davix3f/gASE && cd gASE && git checkout dev") == 0:
            cd("gASE/src")
            print("Repository cloned!")
        else:
            print("Error during repo cloning")
            shell("rm -rf gASE")
            exit()


        # compile
        copyfile("main.py", "main.pyx")
        print(listdir(pwd()))

        def choose_python_version():
            def choice():
                        p_versions=[]
                        for item in listdir("/usr/include"):
                            if "python" in item:
                                p_versions.append(item)
                        p_versions.sort()

                        print("Select the Python version you want for compiling. These have been found in /usr/include:")
                        for key, value in enumerate(p_versions):
                            print("[{0}] -- {1}".format(key, value))
                        print("[QUIT] Abort install")

                        selected = input("User input: ")

                        while selected not in [str(item) for item in range(0, len(p_versions))] + ["QUIT"]:
                            selected = input("User input")
                        if selected == "QUIT":
                            error_occured = True
                            exit()
                        selected = int(selected)

                        if selected in range(0, len(p_versions)):
                            if selected >= key:
                                py_version = p_versions[int(selected)]
                        return(py_version)
            choice_result = choice()
            print("You chose", choice_result)

            confirm = input("Confirm? [y]/[n]: ")
            while confirm not in ["y","n"]:
                confirm = input("Confirm? [y]/[n] ")
            if confirm == "y":
                return(choice_result, "/usr/include/"+choice_result)
            if confirm == "n":
                choose_python_version()

        selected_version = choose_python_version()

        shell("cython main.pyx --embed")

        command = ("gcc -Os -I {0} -o gase main.c -l{1} -lpthread -lm -util -ldl".format(selected_version[1], selected_version[0]))

        print("Performing compilation. The command is \n%s\n. This may take some time" % command)
        if shell(command) == 0 and os.path.isfile("gase"):
            print("\n--#-- Compilation successful --#--\n")
        else:
            print("Some error occurred during compilation. Exiting")
            exit()


        # create dir(s) in opt
        dirs = ["/opt/gase/", "/opt/gase/bin", "/opt/gase/var"]
        for item in dirs:
            if os.path.isdir(item) is not True:
                makedirs(item)

        # copy compiled file in opt/gase + other files
        for item in listdir(pwd):
            if item != "main.py":
                if re.match(r"(\.py)$", item):
                    copy(item, "/opt/gase/bin")

        copy("content/icon.png", "/opt/gase/var")

        start_script = open("/usr/bin/gase", "w")
        print("Writing the launch file")
        start_script.write("#!/bin/bash\ncd /opt/gase/bin\n./gase")
        start_script.close()

        shell("chmod a+x /usr/bin/gase")

        desktop_file_options = ["#!/usr/bin/env xdg-open","[Desktop Entry]",
                                "Version=1.0","Type=Application",
                                "Name=gASE", "Exec=gase",
                                "StartupNotify=True", "Terminal=False",
                                "Icon=/opt/gase/var/icon.png",
                                "Comment=Edit /etc/apt/sources.list"]

        desktop_file = open("/usr/share/applications/gASE.desktop","w")
        for item in desktop_file_options:
            desktop_file.write(item+"\n")
        print("Desktop file written")
        desktop_file.close()

        print("Finished. You can now launch gASE typing \'gase\' in the terminal. Enjoy!")
except:
        print("error - Deleting temporary folder")
        shell("rm -rf /tmp/gASE")
finally:
        print("successful - Deleting temporary folder")
        shell("rm -rf /tmp/gASE")
