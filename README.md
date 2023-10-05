# jupyter-save-load-vars
Saves and loads variables, typically to and from an [IPython/Jupyter](https://stackoverflow.com/questions/51700425/what-is-the-relation-and-difference-between-ipython-and-jupyter-console) workspace.

[dill](https://pypi.org/project/dill/) is often used for [saving and loading from python notebooks](https://stackoverflow.com/questions/34342155/how-to-pickle-or-store-jupyter-ipython-notebook-session-for-later) but it fails for objects that cannot be pickled, e.g. hardware objects or generators. It also requires users to wrap the `dill.dump()` in a with open(file): call and does not handle restoring the variables to the workspace from the returned data from `dill.load()`. _** jupyter-save-load-vars**_ is an attempt to make this process as simple as possible.

**jupyter-save-load-vars** supplies two functions, via `from jupyter_save_load_vars import savevars, loadvars`

* `savevars(filename)` finds all local variables, excludes In and Out and any variable that starts with '_' and just skips objects that cannot be picked.

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
from saveloadvars import savevars,loadvars # import the functions
a=1
b=[2,3]
c='string'
o=(i for i in []) # make generator that cannot be pickled
# define a class
class MyClass:
    name = ""
    l=[1,2,3]
cl = MyClass() # create object with this class

print([a,b,c,o,cl])
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
[1, [2, 3], 'string', <generator object <genexpr> at 0x00000211B426B6D0>, <__main__.MyClass object at 0x00000211B2218130>]
saving variables
deleting b,c
loading variables with prompt (default)
[INFO]: 2023-10-05 14:12:04,992 - saveloadvars - saved to testvars.dill variables [ a b c cl ] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 132, in savevars)
[WARNING]: 2023-10-05 14:12:04,992 - saveloadvars - could not pickle: ['o'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 134, in savevars)
[INFO]: 2023-10-05 14:12:04,994 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 190, in loadvars)
Overwrite existing variable "a" ?  (Yes/no/always): 
Overwrite existing variable "cl" ?  (Yes/no/always): 
loading variables with no overwrite
loading variables with overwrite
[1, [2, 3], 'string', <__main__.MyClass object at 0x00000211B426D610>]
[INFO]: 2023-10-05 14:12:09,437 - saveloadvars - overwrote existing variables ['a', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 224, in loadvars)
[INFO]: 2023-10-05 14:12:09,437 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 190, in loadvars)
[INFO]: 2023-10-05 14:12:09,438 - saveloadvars - did not overwrite existing variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 226, in loadvars)
[INFO]: 2023-10-05 14:12:09,438 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 190, in loadvars)
[INFO]: 2023-10-05 14:12:09,438 - saveloadvars - overwrote existing variables ['a', 'b', 'c', 'cl'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 224, in loadvars)
```


