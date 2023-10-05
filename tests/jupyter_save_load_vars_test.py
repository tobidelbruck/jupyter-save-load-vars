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

