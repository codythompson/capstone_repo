from sys import argv
from sys import stdout
import time

def get_input_filename(command_args):
    for arg in command_args:
        split_arg = arg.split("=", 1)
        if split_arg[0] == "from":
            return split_arg[1]
    return None

#TODO: Make this function not rely on the 'to=' label
def get_output_filename(command_args):
    for arg in command_args:
        split_arg = arg.split("=", 1)
        if split_arg[0] == "to":
            return split_arg[1]
    return None

if len(argv) != 3:
    print "USAGE: python a.py <input filename> <output filename>"
else:
    in_name = get_input_filename(argv)
    out_name = get_output_filename(argv)
    f_in = open(in_name, "r")
    lines = f_in.readlines()
    lines.append("RAN: b\n")

    f_out = open(out_name + ".mmk", "w")
    f_out.writelines(lines)

    print "TOOL B"
    for i in range(11):
        print str(i * 10) + "%"
        stdout.flush()
        time.sleep(.5)
