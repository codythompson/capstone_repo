import glob
import os
import shutil
import subprocess
import sys

#
# constants
#
"""
the keyword to determine when args for this tool stop, and args for the isis
tool begin
"""
tool_arg_start_keyword = "start"

"""
keywords for input and output filenames
"""
input_filename_key = "from"
output_filename_key = "to"

"""
value for args that should be removed
"""
none_value = "None"

"""
flag for copying the input file to the output filename
used when no output file is created by the tool
"""
in_is_out_key = "in_is_out"
in_is_out_value_true = "true"

"""
exclusion keyword
"""
exclusion_key = "exclusion"

#
#functions
#
def print_error(message, exit_after = False, exit_code = 1):
    """
    writes 'message' to standard-error
    if 'exit_after' is true, will exit with the code
    supplied by 'exit_code'
    """
    sys.stderr.write(sys.argv[0] + " - ERROR: " + message + "\n")
    if exit_after:
        exit(exit_code)

def contains_intermediary_args(args):
    """
    checks the arg list for the existence of the keyword used for separating
    arguments for isisToolExecutor.py and arguments for the actual ISIS tool
    """
    for arg in args:
        if arg == tool_arg_start_keyword:
            return True
    return False

def split_args(args):
    for i in range(len(args)):
        if args[i] == tool_arg_start_keyword:
            return args[:i], args[i + 1:]
    return [], args

def parse_inter_args(inter_args_list):
    exclusions = {}
    new_inter_args = {}
    i = 0
    while i < len(inter_args_list):
        split_arg = inter_args_list[i].split("=", 1)
        if len(split_arg) == 2:
            if split_arg[0] == exclusion_key:
                new_excl = {}
                split_excl = split_arg[1].split("=", 1)
                if len(split_excl) == 2:
                    new_excl["value"] = split_excl[1]
                    excl_list = inter_args_list[i + 1].split("=", 1)
                    if len(excl_list) == 2 and excl_list[0] == split_excl[0]:
                        new_excl["excludes"] = excl_list[1].split(',')
                        exclusions[split_excl[0]] = new_excl
                        i = i + 2
                    else:
                        print_error("Invalid exclusion list format.", True)
                else:
                    print_error("Invalid exclusion format.", True)
            else:
                new_inter_args[split_arg[0]]= split_arg[1]
                i = i + 1
        else:
            error_mess = "Unable to parse arg '" + inter_args_list[i] 
            error_mess = error_mess + "' - No '=' found."
            print_error(error_mess, True)
    return exclusions, new_inter_args

def parse_args(args):
    """
    returns a dictionary of arguments meant for this script (isisToolExecutor.py)
    and a list of ISIS tool name and arguments for that tool
    """
    # if no start keyword - use all command line args for the tool
    if not contains_intermediary_args(args):
        return {}, args

    exclusions = []
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

def get_input_filename(tool_args):
    """
    finds the input filename in the supplied ISIS tool arguments
    Uses the label 'from='.
    """
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if split_arg[0].lower() == input_filename_key.lower():
            return split_arg[1]
    return None

def get_output_filename(tool_args):
    """
    finds the output filename in the supplied ISIS tool arguments
    Uses the label 'to='.
    """
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if split_arg[0].lower() == output_filename_key.lower():
            return split_arg[1]
    return None

def remove_args_with(tool_args, remove_with_value):
    """
    Returns a list of ISIS tool args where all occurences of args whose value is
    'remove_with_value' are removed.
    Example, supplying the following as 'tool_args', and 'None' as 'remove_with_value'
    ['ctxcal', 'from=dataset_100.dat', 'to=dataset_101.dat', 'flatfile=None', 'iof=true']
    would result in the following
    ['ctxcal', 'from=dataset_100.dat', 'to=dataset_101.dat', 'iof=true']
    """
    new_args = []
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if not(len(split_arg) == 2 and split_arg[1].lower() == remove_with_value.lower()):
            new_args.append(arg)
    return new_args

def remove_empty_args(tool_args):
    """
    Returns a list of ISIS tool args where all occurences of args whose value is
    empty are removed.
    Example, supplying the following as 'tool_args'
    ['ctxcal', 'from=dataset_100.dat', 'to=dataset_101.dat', 'flatfile=""', 'iof=true']
    would result in the following
    ['ctxcal', 'from=dataset_100.dat', 'to=dataset_101.dat', 'iof=true']
    """
    new_args = []
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if not(len(split_arg) == 2 and split_arg[1] == ""):
            new_args.append(arg)
    return new_args

def remove_exlusions(tool_args, exclusions):
    to_exclude = []
    for arg in tool_args:
        split_arg = arg.split("=", 1)
        if (split_arg[0] in exclusions and
                split_arg[1] == exclusions[split_arg[0]]["value"]):
            to_exclude.extend(exclusions[split_arg[0]]["excludes"])
    new_args = []
    if len(to_exclude) > 0:
        print "!!!!!!!!!"
        print to_exclude
        print "!!!!!!!!!"
        for arg in tool_args:
            arg_key = arg.split("=", 1)[0]
            if not(arg_key in to_exclude):
                new_args.append(arg)
    return new_args

def copy_input_to_output(input_filename, output_filename):
    """
    Just copies a file to a new filename.
    Used for spiceinit and similar tools that do not have a way to specify an
    output filename. (Galaxy requires an output file be generated to function
    properly)
    """
    shutil.copyfile(input_filename, output_filename)

#TODO don't copy all instances to the same filename - gracefully handle that case
def rename_extra_extensions(file_path,
        delete_files_with_extra_extensions = True):
    """
    Finds files that start with 'file_path' but have extra extensions appended
    to the file name, and copy those files to the file name specified by 'file_path'
    
    if 'delete_files_with_extra_extensions' is true - will delete all instances
    of files found with extra extensions after they have been copied to the
    appropriate filename.
    """
    extra_files = glob.glob(file_path + ".*")
    if len(extra_files) > 0:
        shutil.copyfile(extra_files[0], file_path)
        if delete_files_with_extra_extensions:
            for f in extra_files:
                os.remove(f)

def main():
    if len(sys.argv) < 2:
        print_error("Error: Expected at least 2 arguments")
        print_error("format:\npython %s <ISIS Tool> <ISIS Tool args>" % sys.argv[0])
        print_error("or\npython %s <intermediate args> start <ISIS Tool> <ISIS Tool args>" % sys.argv[0], True)
    else:
        #parse the arguments to get the args for isisToolExecutor and the
        #tool name and args for the actual ISIS tool
        #then remove args whose value is 'None', empty, or in the exclude list.
        intermediary_args, tool_args = parse_inter_args(sys.argv[1:])
        tool_args = remove_args_with(tool_args, none_value)
        tool_args = remove_empty_args(tool_args)

        #print the arguments the tool received for debug purposes
        print "Intermediary Script Args Received:"
        print repr(intermediary_args)
        print "ISIS Tool Args Received:"
        print repr(tool_args)

        #Run the ISIS tool and wait for it to finish executing
        sub_proc = subprocess.Popen(tool_args)
        sub_proc.communicate()

        input_path = get_input_filename(tool_args)

        #if specified in the intermediary args - copy the input file to the
        #output file supplied. 
        #used for spiceinit which does not create an output file
        if in_is_out_key in intermediary_args and intermediary_args[in_is_out_key] == in_is_out_value_true:
            output_path = intermediary_args[output_filename_key]
            copy_input_to_output(input_path, output_path)
        else:
            output_path = get_output_filename(tool_args)

        #find files with and extensions appended to the filename and rename them
        #to what Galaxy wanted the output path to be.
        #
        #this is here because many ISIS tools append an extension when the
        #appropriate extension was not supplied in the output file name.
        #example:
        #ctxcal from='dataset_101.dat' to='dataset_102.dat'
        #would result in a file named: 'dataset_102.dat.cub'
        #and galaxy is expecting a file named 'dataset_102.dat' to exist
        rename_extra_extensions(output_path)

def test_main():
    #split the args into args for this script and args for the isis tool
    inter_args, tool_args = split_args(sys.argv[1:])
    #grab the exclusions and regular args for this script
    exclusions, inter_args = parse_inter_args(inter_args)
    #remove all 'None' valued, empty, and args that should be excluded
    tool_args = remove_exlusions(tool_args, exclusions)
    tool_args = remove_args_with(tool_args, none_value)
    tool_args = remove_empty_args(tool_args)
    print "Exclusions:"
    print repr(exclusions)
    print "Inter Args:"
    print repr(inter_args)
    print "Tool Args"
    print repr(tool_args)
    
    #Run the ISIS tool and wait for it to finish executing
    sub_proc = subprocess.Popen(tool_args)
    sub_proc.communicate()

    input_path = get_input_filename(tool_args)

    #if specified in the intermediary args - copy the input file to the
    #output file supplied. 
    #used for spiceinit which does not create an output file
    if in_is_out_key in intermediary_args and intermediary_args[in_is_out_key] == in_is_out_value_true:
        output_path = intermediary_args[output_filename_key]
        copy_input_to_output(input_path, output_path)
    else:
        output_path = get_output_filename(tool_args)

    #find files with and extensions appended to the filename and rename them
    #to what Galaxy wanted the output path to be.
    #
    #this is here because many ISIS tools append an extension when the
    #appropriate extension was not supplied in the output file name.
    #example:
    #ctxcal from='dataset_101.dat' to='dataset_102.dat'
    #would result in a file named: 'dataset_102.dat.cub'
    #and galaxy is expecting a file named 'dataset_102.dat' to exist
    rename_extra_extensions(output_path)

if __name__ == '__main__':
    test_main()
