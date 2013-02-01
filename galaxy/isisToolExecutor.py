import sys
import subprocess

def get_input_filename(command_args):
    for arg in command_args:
        split_arg = arg.split("=", 1)
        if split_arg[0] == "from":
            return split_arg[1]
    return None

def get_output_filename(command_args):
    for arg in command_args:
        split_arg = arg.split("=", 1)
        if split_arg[0] == "to":
            return split_arg[1]
    return None

def main():
    if len(sys.argv) < 2:
        # TODO: a better error message - maybe a usage statement
        sys.stderr.write("Error: Expected at least 2 arguments")
    else:
        command_args = sys.argv[1:]

        #TEST CODE - REMOVE LATER
        print command_args
        print "input fname: " + get_input_filename(command_args)
        print "output fname: " + get_output_filename(command_args)

#        sub_proc = subprocess.Popen(command_args)
#        sub_proc.communicate()

if __name__ == '__main__':
    main()
