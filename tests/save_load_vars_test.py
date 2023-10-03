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

print(a)
print(b)
print(c)
