class ToolArgInfo:
    def __init__(self, arg_name, arg_prefix, arg_postfix):
        self.arg_name = arg_name
        self.prefix = arg_prefix
        self.postfix = arg_postfix

class ToolInfo:
    def __init__(self, interpreter, command, input_arg_info, output_arg_info):
        self.interpreter = interpreter
        self.command = command
        self.input_arg_info = input_arg_info
        self.output_arg_info = output_arg_info

#TODO: change this to handle more command line arg configurations than just
# one input and one output
def build_args(tool_info, input_fname, output_fname):
    args = []

    if len(tool_info.interpreter) > 0:
        args.append(tool_info.interpreter)

    args.append(tool_info.command)
    args.append(input_fname)
    args.append(output_fname)

    return args

#TODO: change this to handle more command line arg configurations than just
# one input and one output
def build_step_tuples(selected_tools, first_input_filename):
    prev_tuple = None
    for i in reversed(range(len(selected_tools))):
        in_fname = None
        if not i == 0:
            in_fname = "out_" + str(i - 1) + ".txt" #TODO use correct extension
        else:
            in_fname = first_input_filename
        out_fname = "out_" + str(i) + ".txt" #TODO use correct extension
        args = build_args(selected_tools[i], in_fname, out_fname)
        step_tuple = None
        if (i == len(selected_tools)):
            step_tuple = (args,)
        else:
            step_tuple = (args, prev_tuple)
        prev_tuple = step_tuple
    return prev_tuple
