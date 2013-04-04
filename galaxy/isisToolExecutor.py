import glob
import os
import shutil
import subprocess
import sys

#
# constants
#
#might want to move this section to a new module to make it more like constants

#the keyword to determine when args for this tool stop, and args for the isis
#tool begin
tool_arg_start_keyword = "start"

#keywords for input and output filenames
input_filename_key = "from"
output_filename_key = "to"

#value for None values that get removed
none_value = "None"

# arg for copying the input file to the output filename
# used when no output file is created by the tool
in_is_out_key = "in_is_out"
in_is_out_value_true = "true"

#
#functions
#
def print_error(message, exit_after = False, exit_code = 1):
    sys.stderr.write(sys.argv[0] + " - ERROR: " + message + "\n")
    if exit_after:
        exit(exit_code)

def contains_intermediary_args(args):
    for arg in args:
        if arg == tool_arg_start_keyword:
            return True
    return False

def parse_args(args):
    # if no start keyword - use all command line args for the tool
    if not contains_intermediary_args(args):
        return {}, args

    intermediary_args = {}
    tool_args = []
    reading_tool_args = False
    for arg in args:
        if arg == tool_arg_start_keyword:
            reading_tool_args = True
        elif reading_tool_args:
            tool_args.append(arg)
        else:
            split_arg = arg.split("=", 1)
            if len(split_arg) == 2:
                intermediary_args[split_arg[0]] = split_arg[1]
            else:
                print_error("Unable to parse arg '" + arg + "' - No '=' found.")
    return intermediary_args, tool_args

#TODO: Make this function not rely on the 'from=' label
def get_input_filename(tool_args):
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if split_arg[0].lower() == input_filename_key.lower():
            return split_arg[1]
    return None

#TODO: Make this function not rely on the 'to=' label
def get_output_filename(tool_args):
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if split_arg[0].lower() == output_filename_key.lower():
            return split_arg[1]
    return None

def remove_args_with_value_none(tool_args):
    new_args = []
    for arg in tool_args:
       split_arg = arg.split("=", 1) 
       if not(len(split_arg) == 2 and split_arg[1].lower() == none_value.lower()):
          new_args.append(arg)
    return new_args

def copy_input_to_output(input_filename, output_filename):
    shutil.copyfile(input_filename, output_filename)

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
        intermediary_args, tool_args = parse_args(sys.argv[1:])
        tool_args = remove_args_with_value_none(tool_args)

        print repr(tool_args)

#        sub_proc = subprocess.Popen(tool_args)
#        sub_proc.communicate()
#
#        input_path = get_input_filename(tool_args)
#
#        if in_is_out_key in intermediary_args and intermediary_args[in_is_out_key] == in_is_out_value_true:
#            output_path = intermediary_args[output_filename_key]
#            copy_input_to_output(input_path, output_path)
#        else:
#            output_path = get_output_filename(tool_args)

#        if not os.path.exists(output_path):
#            rename_extra_extensions(output_path)
#TODO Don't always rename the files with extra extensions
#        rename_extra_extensions(output_path)

if __name__ == '__main__':
    main()
