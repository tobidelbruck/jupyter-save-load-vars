# from jupyter_save_load_vars import _yes_or_no_or_always
# print(_yes_or_no_or_always('_yes_or_no_or_always test?'))
# print(_yes_or_no_or_always('_yes_or_no_or_always test?',always_option=False))

from jupyter_save_load_vars import savevars,loadvars,printvars
a=1
b=[2,3]
c='string'
o=(i for i in []) # make generator that cannot be pickled
In=[1,2,'3']
Out=['an Out string']
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
print('saving all variables')
savevars('testvars')
print('saving only b,c variables')
savevars('partvars',['b','c'])

print('deleting b,c')
del b,c
print('loading variables with prompt (default)')
loadvars('testvars') # load with prompt for overwriting existing a variable
# loadvars(filename,warn=False) # suppresses warning about unsafe unpickling
print('loading variables with no overwrite')
loadvars('testvars',overwrite='no')
print('loading variables with overwrite')
loadvars('testvars',overwrite='yes')
printvars()
del a,b,c,cl,o
print('loading only b,c saved earlier')
loadvars('partvars')
printvars()

