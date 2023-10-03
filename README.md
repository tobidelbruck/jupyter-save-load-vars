# saveloadvars
Saves and loads variables, typically to and from an IPython/Jupyter workspace.

Usage:
```python
from saveloadvars import savevars,loadvars
a=1
b=[2,3]
c='string'
o=(i for i in []) # make generator that cannot be pickled
print([a,b,c,o])
savevars('testvars')

del b,c
loadvars('testvars',overwrite='no')
loadvars('testvars',overwrite='yes')
del a,b
loadvars('testvars',overwrite='prompt')

```

Output:
```
[1, [2, 3], 'string', <generator object <genexpr> at 0x0000021141A4E740>]
[INFO]: 2023-10-03 13:18:05,182 - NE1 - saved to testvars.dill variables [ a b c ] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 131, in savevars)
[WARNING]: 2023-10-03 13:18:05,182 - NE1 - could not pickle: ['o'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 133, in savevars)
[INFO]: 2023-10-03 13:18:05,188 - NE1 - from testvars.dill loaded variables ['a', 'b', 'c'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
[INFO]: 2023-10-03 13:18:05,188 - NE1 - did not overwrite existing variables ['a'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 198, in loadvars)
[INFO]: 2023-10-03 13:18:05,188 - NE1 - from testvars.dill loaded variables ['a', 'b', 'c'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
[INFO]: 2023-10-03 13:18:05,188 - NE1 - overwrote existing variables ['a', 'b', 'c'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 196, in loadvars)
[INFO]: 2023-10-03 13:18:05,188 - NE1 - from testvars.dill loaded variables ['a', 'b', 'c'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 162, in loadvars)
[WARNING]: 2023-10-03 13:18:05,188 - NE1 - cannot use timeout signal on windows (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 251, in _yes_or_no_or_always)
Overwrite existing variable "c" ?  (Yes/no): n
1
[2, 3]
string
[INFO]: 2023-10-03 13:18:09,538 - NE1 - did not overwrite existing variables ['c'] (File "F:/tobi/Dropbox (Personal)/GitHub/tobidelbruck/saveloadvars/saveloadvars.py", line 198, in loadvars)

```


