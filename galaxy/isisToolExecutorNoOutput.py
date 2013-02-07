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

def remove_output_filename_from_args(command_args):
    output_filename = None
    new_args = []
    for arg in command_args:
        split_arg = arg.split("=", 1)
        if split_arg[0] ==  "to":
            output_filename = split_arg[1]
        else:
            new_args.append(arg)
    return (output_filename, new_args)

def rename_extra_extensions(file_path,
        delete_files_with_extra_extensions = True):
    extra_files = glob.glob(file_path + ".*")
    if len(extra_files) > 0:
        shutil.copyfile(extra_files[0], file_path)
        if delete_files_with_extra_extensions:
            for f in extra_files:
                os.remove(f)

def copy_input_to_output(input_filename, output_filename):
    shutil.copyfile(input_filename, output_filename)

def main():
    if len(sys.argv) < 2:
        # TODO: a better error message - maybe a usage statement
        sys.stderr.write("Error: Expected at least 2 arguments")
    else:
        command_args = sys.argv[1:]
        output_path, command_args = remove_output_filename_from_args(command_args)
        input_path = get_input_filename(command_args)

        #TEST CODE - REMOVE LATER
        print "command: " + command_args[0]
        print "input fname: " + input_path
        print "output fname: " + output_path
        print "all args: " + repr(command_args)

        sub_proc = subprocess.Popen(command_args)
        sub_proc.communicate()

#        if not os.path.exists(output_path):
#            rename_extra_extensions(output_path)
        rename_extra_extensions(output_path)
        copy_input_to_output(input_path, output_path)


if __name__ == '__main__':
    main()
