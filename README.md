RunM
=================

RunM is an opinionated version of `subprocess`, making it just that little
bit more convenient to run shell commands from within Python code.

It is reasonably straightforward:
```
import runm
runm.run("echo it works") #=> returns 'it works\n'
runm.run("echo 1 2 5 |cat") #=> returns '1 2 5\n'
```
When a command that fails is run e.g.
```
runm.run("cat /not_a_file")
```
an exception is raised just like `subprocess`. However, the error message
generated includes STDERR and STDOUT, which is more convenient for debugging.

Installation
--------------

commandeer can be installed by unzipping the source code in one directory and using this command: ::

    sudo python setup.py install

You can also install it directly from the Python Package Index with this command: ::

    sudo pip install runm


Licence
--------

See file LICENCE.txt in this folder


Contribute
-----------
RunM is an open-source software. Everyone is welcome to contribute !
