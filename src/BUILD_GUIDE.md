# Requirements
**System packages:** [sudo apt install <package name>]
* `python-dev` or `python3-dev`, depending on what Python version you want to use. The application is written on Python3, so python3-dev is recommended.

**Python packages:** [sudo pip install <package name>]
* `gi`

## How to compile for binary package
This guide is for Python3. If you want to build the binary on Python2.7, change all of the "python3.5m" with "python2.7" or whatever version you have.
You can have a full list of Python versions you have installed with the command `ls /usr/include | grep python`

1. Copy `main.py` (or its content) as a **.pyx** file, and the other .py files with no changes. They have to be in the same folder with the .pyx file.
2. Using **cython** (install it with `sudo pip install cython`):
`cython main.pyx --embed`
3. Compile the C file you got as output:
`gcc -Os -I /usr/include/python3.5m file.c -lpython3.5m -lpthread -lm -lutil -ldl`
This will output a file called `a.out`. If you want a different output name, you have to add the `-o` flag:
`gcc -Os -I /usr/include/python3.5m -o [/eventual/path/file_name] file.c -lpython3.5m -lpthread -lm -lutil -ldl`

4. Now, execute the file you got as output: `./[filename]` 
