# How to compile for binary package


1. Copy `main.py` (or its content) as a **.pyx** file, and the other .py files with no changes. They have to be in the same folder with the .pyx file.
2. Using **cython** (install it with `sudo pip install cython`):
`cython main.pyx --embed`
3. Compile the C file you got as output:
`gcc -Os -I /usr/include/python3.5m file.c -lpython3.5m -lpthread -lm -lutil -ldl`
This will output a file called `a.out`. If you want a different output name, you have to add the `-o` flag:
`gcc -Os -I /usr/include/python3.5m -o [/eventual/path/file_name] file.c -lpython3.5m -lpthread -lm -lutil -ldl`

4. Now, execute the file you got as output: `./[filename]` 
