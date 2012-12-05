class ToolArgInfo:
    def __init__(self, arg_name, arg_prefix, arg_postfix, file_extension):
        self.arg_name = arg_name
        self.prefix = arg_prefix
        self.postfix = arg_postfix
        self.file_extension = file_extension

    def get_arg_string(self, arg_value, add_extension=True):
        arg_string = self.prefix + arg_value
        if add_extension:
            arg_string = arg_string + self.file_extension
        arg_string = arg_string + self.postfix
        return arg_string

class ToolInfo:
    def __init__(self, interpreter, command, input_arg_info, output_arg_info):
        self.interpreter = interpreter
        self.command = command
        self.input_arg_info = input_arg_info
        self.output_arg_info = output_arg_info

    #TODO: change this to handle more command line arg configurations than just
    # one input and one output
    def build_args(self, input_filename, output_filename, 
            add_extension_to_input=False, add_extension_to_output=True):
        args = []

        if len(self.interpreter) > 0:
            args.append(self.interpreter)

        args.append(self.command)
        args.append(self.input_arg_info.get_arg_string(input_filename,
            add_extension_to_input))
        args.append(self.output_arg_info.get_arg_string(output_filename,
            add_extension_to_output))

        return args

#TODO: change this to handle more command line arg configurations than just
# one input and one output
#TODO: do some file extension checking to insure that the input/outputs are
# compatible
def build_step_tuples(selected_tools, first_input_filename):
    prev_tuple = None
    for i in reversed(range(len(selected_tools))):
        in_fname = "out_" + str(i - 1)
        add_input_extension = True
        if i == 0:
            in_fname = first_input_filename
            add_input_extension = False
        out_fname = "out_" + str(i) 
        args = selected_tools[i].build_args(in_fname, out_fname,
            add_extension_to_input=add_input_extension)
        step_tuple = (args, prev_tuple)
        if (i == len(selected_tools)):
            step_tuple = (args,)
        prev_tuple = step_tuple
    return prev_tuple
