################################################################################
# module tool_info.py
#
# Classes used for storing information about command line tools and
# creating argument lists for executing the tools.
################################################################################

################################################################################
# Class ToolArgInfo
#
# Stores information about a command line input argument for a command line tool
# Builds a string that can be used as an argument for a command line tool.
################################################################################
class ToolArgInfo:

    # Constructor
    #
    # params:
    # arg_name - A string containing the name of the argument. This is not
    #           this is not currently used for anything
    # arg_prefix - A string containing any prefix that the command line argument
    #               might use. (ex "from=" )
    #               If this tool does not need a prefix empty quotes can be used
    # arg_postfix - Same as the prefix but comes after the argument
    #               If this tool does not need a postfix empty quotes can be
    #               used.
    # file_extension - A string containing the file extension for the
    #                   input/output. (ex ".txt")
    #                   TODO: don't require the leading period.
    def __init__(self, arg_name, arg_prefix, arg_postfix, file_extension):
        self.arg_name = arg_name
        self.prefix = arg_prefix
        self.postfix = arg_postfix
        self.file_extension = file_extension

    # Returns a string that can be used as a command line argument.
    #
    # params:
    # arg_value - A string that is the value for the argument
    #               (ex: "somefilename" or "somefilename.txt")
    # add_extension - A boolean. If true will append the file extension given to
    #                   to the contructor to the end of the arg_value
    #                   defaults to True
    def get_arg_string(self, arg_value, add_extension=True):
        arg_string = self.prefix + arg_value
        if add_extension:
            arg_string = arg_string + self.file_extension
        arg_string = arg_string + self.postfix
        return arg_string

################################################################################
# Class ToolInfo
#
# Stores information used to create a list of strings that can be used to 
# execute a program or script.
#
# TODO: support for shell=True or shell=False for subprocess.popen
################################################################################
class ToolInfo:
    # Constructor
    #
    # params:
    # interpreter - A string containing the name of the interpreter (if any)
    #               that will run the tool as it appears on the command line.
    #               (ex: "python")
    #               If no interpreter supply an empty string
    # command - A string containing the name of the tool as it would appear
    #           on the command line. (ex "mroctx2isis" or "somepythonscript.py")
    # input_arg_info - An instance of ToolArgInfo that represents the input
    #                   file argument for the tool
    # output_arg_info - An instance of ToolArgInfo that represents the output
    #                   file argument for the tool. If the tool has no output
    #                   argument you should supply None or empty quotes
    def __init__(self, interpreter, command, input_arg_info, output_arg_info):
        self.interpreter = interpreter
        self.command = command
        self.input_arg_info = input_arg_info
        self.output_arg_info = output_arg_info

    # Returns an array of strings that can be given to subprocess.popen or
    # something similar that will execute the program.
    #
    # params:
    # input_filename - the name of the file that this tool should use as input.
    # output_filename - the filename that this tool should use for it's output
    #                   file.
    # add_extension_to_input - whether or not to add a file extension to the
    #                           given input filename.
    #                           Defaults to False
    # add_extension_to_output - whether or not to add a file extension to the
    #                           given output filename.
    #                           Defaults to True
    def build_args(self, input_filename, output_filename, 
            add_extension_to_input=False, add_extension_to_output=True):
        args = []

        if len(self.interpreter) > 0:
            args.append(self.interpreter)

        args.append(self.command)
        args.append(self.input_arg_info.get_arg_string(input_filename,
            add_extension_to_input))

        if self.output_arg_info:
            args.append(self.output_arg_info.get_arg_string(output_filename,
                add_extension_to_output))

        return args

    # Returns the name of the output file that will be produced by this tool.
    #
    # params:
    # you should supply the same params you supplied to a call to bulid_args
    def get_output_filename(self, input_filename, output_filename, 
            add_extension_to_input=False, add_extension_to_output=True):
        if self.output_arg_info:
            return self.output_arg_info.get_arg_string(output_filename,
                    add_extension_to_output)
        else:
            return self.input_arg_info.get_arg_string(input_filename,
                    add_extension_to_input)
