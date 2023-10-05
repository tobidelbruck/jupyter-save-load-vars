from saveloadvars import savevars,loadvars
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

