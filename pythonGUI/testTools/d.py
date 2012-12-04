from sys import argv

if len(argv) != 2:
    print "USAGE: python d.py <input filename>"
else:
    f = open(argv[1], "a")
    f.write("RAN: d\n")
