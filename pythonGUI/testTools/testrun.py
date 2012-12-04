from subprocess import Popen
from sys import path

path.append("../")

from workflow import *

#Popen(['python', 'a.py', 'out\\orig.txt', 'out\\aa.txt'])
#Popen(['python', 'b.py', 'out\\aa.txt', 'out\\ab.txt'])
#Popen(['python', 'c.py', 'out\\ab.txt', 'out\\ac.txt'])


c_tup = (['python', 'c.py', 'out\\ab.txt', 'out\\ac.txt'],)
b_tup = (['python', 'b.py', 'out\\aa.txt', 'out\\ab.txt'], c_tup)
a_tup = (["python", "a.py", "out\\orig.text", "out\\aa.txt"], b_tup)

print "a tup:"
print a_tup[0]
print "b tup:"
print b_tup[0]
print "c tup:"
print c_tup[0]

run_workflow(a_tup)
