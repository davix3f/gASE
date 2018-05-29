from os import system as shell
from os import makedirs
from os import listdir
import os.path
from shutil import copyfile, copy
from shutil import copytree as copydir
from getpass import getuser


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

            confirm = input("Confirm? [y]/[n]")
            while confirm not in ["y","n"]:
                confirm = input("Confirm? [y]/[n]")
            if confirm == "y":
                return(choice_result, "/usr/include/"+choice_result)
            if confirm == "n":
                choose_python_version()

        selected_version = choose_python_version()

        shell("cython main.pyx --embed")

        command = ("gcc -Os -I {0} -o gase main.c -l{1} -lpthread -lm -util -ldl".format(selected_version[1], selected_version[0]))
        if shell(command) == 0 and os.path.isfile("gase"):
            print("\n--#-- Compilation successful --#--\n")
        else:
            print("Some error occurred during compilation. Exiting")
            exit()


        # create dir in opt
        if os.path.isdir("/opt/gase") is not True:
            os.makedirs("/opt/gase")
        else:
            print("Folder /opt/gase already existing")
        if os.path.isdir("/opt/gase/bin") is not True:
            os.makedirs("/opt/gase/bin")
        if os.path.isdir("/opt/gase/var") is not True:
            os.makedirs("/opt/gase/var")

        # copy compiled file in opt/gase
        copy("gase", "/opt/gase/bin")
        copy("line_analysis.py", "/opt/gase/bin")
        copy("content/icon.png", "opt/gase/var")
        if os.path.isfile("/opt/gase/bin/gase") is True and os.path.isfile("/opt/gase/bin/line_analysis.py") is True:
            print("Files successfully copied to opt folder")
        else:
            print("Files not copied")
            exit()

        with open("/usr/bin/gase", "w") as start_script:
            print("Writing the launch file")
            start_script.write("#!/bin/bash\ncd /opt/gase/bin\n./gase")
        start_script.close()

        shell("chmod a+x /usr/bin/gase")

        desktop_file_options = ["[Desktop Entry]", "Name=gASE", "Exec=gASE", "StartupNotify=True", "Terminal=false", "Type=Application","/opt/gase/var/icon.png"]
        with open ("/usr/share/applications/gASE.desktop","w") as desktop_file:
            for item in desktop_file_options:
                desktop_file.write(item+"\n")
        desktop_file.close()

        print("Emptying repo from tmp")
        print("Finished. You can now launch gASE typing \'gase\' in the terminal. Enjoy!")
except:
        print("Deleting temporary folder")
        shell("rm -rf /tmp/gASE")
finally:
        print("Deleting temporary folder")
        shell("rm -rf /tmp/gASE")
