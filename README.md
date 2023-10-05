# jupyter-save-load-vars
Saves and loads variables, typically to and from an [IPython/Jupyter](https://stackoverflow.com/questions/51700425/what-is-the-relation-and-difference-between-ipython-and-jupyter-console) workspace.

[dill](https://pypi.org/project/dill/) is often used for [saving and loading from python notebooks](https://stackoverflow.com/questions/34342155/how-to-pickle-or-store-jupyter-ipython-notebook-session-for-later) but it fails for objects that cannot be pickled, e.g. hardware objects or generators. It also requires users to wrap the `dill.dump()` in a with open(file): call and does not handle restoring the variables to the workspace from the returned data from `dill.load()`. _** jupyter-save-load-vars**_ is an attempt to make this process as simple as possible.

**jupyter-save-load-vars** supplies two functions, via `from jupyter_save_load_vars import savevars, loadvars`

* `savevars(filename, overwrite='prompt')` finds all local variables, excludes In and Out and any variable that starts with '_' and just skips objects that cannot be picked. _overwrite_ can be 'prompt' (the default), 'yes' (to silently overwrite), or 'no' to not overwrite existing data file.

* `loadvars(filename, overwrite='prompt')` loads the variables back into the workspace. _overwrite_ can be 'prompt' (the default), 'yes' (to silently overwrite), or 'no' to not overwrite existing variables.

The file name has _.dill_ appended if no suffix is provided.

_jupyter-save-load-vars_ is available from [pypi](https://pypi.org/) and can be installed with
```bash
pip install jupyter-save-load-vars
```
(Note the use of - for install and _ for import)

### Warning
Liike any unpickling operation, users should not `loadvars` from any file whose provenance is unknown.

## Usage:

```python
from jupyter_save_load_vars import savevars,loadvars,printvars
a=1
b=[2,3]
c='string'
o=(i for i in []) # make generator that cannot be pickled
# define a class
class MyClass:
    name = ""
    l=[1,2,3]
cl = MyClass() # create object with this class

import functools, sys
print = functools.partial(print, flush=True, file=sys.stderr) # flush and put print() on stderr so logging comes in sequence

import time
printvars()
time.sleep(3)
print('saving variables')
savevars('testvars')
print('deleting b,c')
del b,c
print('loading variables with prompt (default)')
loadvars('testvars') # load with prompt for overwriting existing a variable
# loadvars(filename,warn=False) # suppresses warning about unsafe unpickling
print('loading variables with no overwrite')
loadvars('testvars',overwrite='no')
print('loading variables with overwrite')
loadvars('testvars',overwrite='yes')
print([a,b,c,cl])
```

### Output:
```
variables: a,b,c,o,cl,
saving variables
file testvars.dill already exists, overwrite it?  [Yes/no/always]: 
[INFO]: 2023-10-05 20:25:32,410 - saveloadvars - saved to testvars.dill variables [ a b c cl ] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 141, in savevars)
[WARNING]: 2023-10-05 20:25:32,410 - saveloadvars - could not pickle: ['o'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 143, in savevars)
deleting b,c
loading variables with prompt (default)
[INFO]: 2023-10-05 20:25:32,412 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 198, in loadvars)
Overwrite existing variable "a" ?  [Yes/no/always]: a
[INFO]: 2023-10-05 20:25:37,640 - saveloadvars - overwrote existing variables ['a', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 232, in loadvars)
loading variables with no overwrite
[INFO]: 2023-10-05 20:25:37,641 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 198, in loadvars)
[INFO]: 2023-10-05 20:25:37,641 - saveloadvars - did not overwrite existing variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 234, in loadvars)
loading variables with overwrite
[INFO]: 2023-10-05 20:25:37,641 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 198, in loadvars)
[INFO]: 2023-10-05 20:25:37,641 - saveloadvars - overwrote existing variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/jupyter-save-load-vars/jupyter_save_load_vars.py", line 232, in loadvars)
[1, [2, 3], 'string', <__main__.MyClass object at 0x0000023A8AD03FA0>]

```


