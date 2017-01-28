Extern
=================

Extern is an opinionated version of Python's `subprocess`, making it just that little
bit more convenient to run shell commands from within Python code.

It is reasonably straightforward:
```
>>> import extern
>>> extern.run("echo it works") #=> returns 'it works\n'
>>> extern.run("echo 1 2 5 |cat") #=> returns '1 2 5\n'
```
When a command that fails is run e.g.
```
>>> extern.run("cat /not_a_file")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "build/bdist.linux-x86_64/egg/extern/__init__.py", line 29, in run
extern.ExternCalledProcessError: Command cat /not_a_file returned non-zero exit status 1.
STDERR was: cat: /not_a_file: No such file or directory
STDOUT was: 
```
an exception is raised just like `subprocess`. However, the error message
generated includes STDERR and STDOUT, which is more convenient for debugging. For reference, the `subprocess` equivalent:
```
>>> subprocess.check_output(['bash','-c','cat /not_a_file'])
cat: /not_a_file: No such file or directory
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/subprocess.py", line 573, in check_output
    raise CalledProcessError(retcode, cmd, output=output)
subprocess.CalledProcessError: Command '['bash', '-c', 'cat /not_a_file']' returned non-zero exit status 1
```
The useful thing is that `Extern` collects STDERR and only reports it when there is a non-zero exit status, discarding it otherwise.

**IMPORTANT**: use of this library with untrusted strings presents a security risk in the same way as [little bobby tables](http://xkcd.com/327/), and [shell=True](https://docs.python.org/2/library/subprocess.html#frequently-used-arguments) in `subprocess`.

###Multiple commands run simultaneously
```
>>> extern.run_many(['echo once','echo twice','echo thrice'])
#=> ['once\n', 'twice\n', 'thrice\n']
```
Progress can also be observed:
```
>>> extern.run_many(['echo once','echo twice','echo thrice'], progress_stream=sys.stderr)
Finished processing 3 of 3 (100.00%) items.
#=> ['once\n', 'twice\n', 'thrice\n']
```
`STDIN` can be provided to `run()`:
```
extern.run('cat',stdin='dog') #=> 'dog'
````

###Which
There is also a `which` function, useful for determing where (and if) a program
exists on the command line:
```
>>> import extern
>>> extern.which('cat') #=> '/bin/cat'
>>> extern.which('dog') #=> None
```


Installation
--------------
You can also install it directly from the Python Package Index with this command:
```
sudo pip install extern
```

Licence
--------
See file LICENCE.txt in this folder

Contribute
-----------
Extern is an open-source software. Everyone is welcome to contribute !
