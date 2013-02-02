import glob
import os
import shutil
import subprocess
import sys

#TODO: Make this function not rely on the 'from=' label
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

def rename_extra_extensions(file_path,
        delete_files_with_extra_extensions = True):
    extra_files = glob.glob(file_path + ".*")
    if len(extra_files) > 0:
        shutil.copyfile(extra_files[0], file_path)
        if delete_files_with_extra_extensions:
            for f in extra_files:
                os.remove(f)

def main():
    if len(sys.argv) < 2:
        # TODO: a better error message - maybe a usage statement
        sys.stderr.write("Error: Expected at least 2 arguments")
    else:
        command_args = sys.argv[1:]
        input_path = get_input_filename(command_args)
        output_path = get_output_filename(command_args)

        #TEST CODE - REMOVE LATER
        print "command: " + command_args[0]
        print "input fname: " + input_path
        print "output fname: " + output_path

        sub_proc = subprocess.Popen(command_args)
        sub_proc.communicate()

#        if not os.path.exists(output_path):
#            rename_extra_extensions(output_path)
        rename_extra_extensions(output_path)

if __name__ == '__main__':
    main()
