# saveloadvars
Saves and loads variables, typically to and from an [IPython/Jupyter](https://stackoverflow.com/questions/51700425/what-is-the-relation-and-difference-between-ipython-and-jupyter-console) workspace.

[dill](https://pypi.org/project/dill/) is often used for [saving and loading from python notebooks](https://stackoverflow.com/questions/34342155/how-to-pickle-or-store-jupyter-ipython-notebook-session-for-later) but it fails for objects that cannot be pickled, e.g. hardware objects or generators. It also requires users to wrap the `dill.dump()` in a with open(file): call and does not handle restoring the variables to the workspace from the returned data from `dill.load()`. _saveloadvars_ is an attempt to make this process as simple as possible.

* `savevars(filename)` finds all local variables, excludes In and Out and any variable that starts with '_' and just skips objects that cannot be picked.

* `loadvars(filename, overwrite='prompt')` loads the variables back into the workspace. _overwrite_ can be 'prompt' (the default), 'yes' (to silently overwrite), or 'no' to not overwrite existing variables.

The file name has _.dill_ added if no suffix is provided.


## Usage:
```python
from saveloadvars import savevars,loadvars
a=1
b=[2,3]
c='string'
o=(i for i in []) # make generator that cannot be pickled
print([a,b,c,o])
savevars('testvars') # saves data to savevars.dill
del b,c
loadvars('testvars',overwrite='no') # loads data back but over overwriting existing variable a
loadvars('testvars',overwrite='yes') # now we overwrite a
del a
loadvars('testvars',overwrite='prompt') # now try the prompt (Yes/no/always)

print(a)
print(b)
print(c)
```

### Output:
```
[1, [2, 3], 'string', <generator object <genexpr> at 0x7f254793b7b0>]
[INFO]: 2023-10-03 16:50:07,541 - saveloadvars - saved to testvars.dill variables [ a b c ] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 131, in savevars)
[WARNING]: 2023-10-03 16:50:07,541 - saveloadvars - could not pickle: ['o'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 133, in savevars)
[INFO]: 2023-10-03 16:50:07,542 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
[INFO]: 2023-10-03 16:50:07,542 - saveloadvars - did not overwrite existing variables ['a'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 198, in loadvars)
[INFO]: 2023-10-03 16:50:07,542 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
[INFO]: 2023-10-03 16:50:07,542 - saveloadvars - overwrote existing variables ['a', 'b', 'c'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 196, in loadvars)
[INFO]: 2023-10-03 16:50:07,542 - saveloadvars - from testvars.dill loaded variables ['a', 'b', 'c'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
Overwrite existing variable "b" ?  (Yes/no/always): a
1
[2, 3]
string
[INFO]: 2023-10-03 16:50:12,722 - saveloadvars - overwrote existing variables ['b', 'c'] (File "/home/tobi/Dropbox/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 196, in loadvars)

```


