from sys import argv
from sys import stdout
import time

if len(argv) != 3:
    print "USAGE: python a.py <input filename> <output filename>"
else:
    f_in = open(argv[1], "r")
    lines = f_in.readlines()
    lines.append("RAN: b\n")

    f_out = open(argv[2], "w")
    f_out.writelines(lines)

    print "TOOL B"
    for i in range(11):
        print str(i * 10) + "%"
        stdout.flush()
        time.sleep(.5)
