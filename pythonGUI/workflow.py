import sys
import subprocess

################################################################################
# Prints the output from a running tool
# params:
# process - the process object returned from the call to subprocess.Popen
################################################################################
def default_workflow_output_handler(process):
    sys.stdout.flush()
    while True:
        next_line = process.stdout.readline()
        if not next_line:
            break
        print "\r" + next_line
        sys.stdout.flush()

################################################################################
# A class that acts as a step in a workflow.
# The run method will execute the tool and call run on the next workflow tool
################################################################################
class WorkflowTool:
    # Constructor
    #
    # params:
    # tool_info - An instance of the ToolInfo class from tool_info.py.
    # output_handler - A function that takes the process object resulting from
    #                  a call to subprocess.Popen and handles output from
    #                  process.stdout or process.stderr.
    #                  Defaults to defualt_workflow_handler(process) above.
    def __init__(self, tool_info, output_handler =
            default_workflow_output_handler):
        self.tool_info = tool_info
        self.output_handler = output_handler
        self.call_when_finished = None

    # sets the function/method to call when finished when the tool finishes 
    # running.
    # params:
    # call_when_finished - the method to call when the tool has finished 
    # running. Should be given the next WorkflowTool objects run method.
    def set_call_when_finished(self, call_when_finished):
        self.call_when_finished = call_when_finished

    # Runs the tool using subprocess.Popen
    #
    # params:
    # input_fname - the filename of the input file that the tool should use.
    # output_base_name - the base file name that should be given to any tool's
    #                    output file, including the output of tools that will
    #                    be run later in the workflow.
    # add_extension_to_input - whether or not to add file extensions to input
    #                          files (for this or following tools)
    #                          Defaults to False.
    # add_extension_to_output - whether or not to add file extensions to output
    #                          files (for this or following tools)
    #                          Defaults to True.
    def run(self, input_fname, output_base_name, add_extension_to_input = False,
            add_extension_to_output = True):
        args = self.tool_info.build_args(input_fname, output_base_name,
                add_extension_to_input, add_extension_to_output)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        self.output_handler(p)
        p.communicate()

        if self.call_when_finished:
            output_fname = self.tool_info.get_output_filename(input_fname,
                    output_base_name, add_extension_to_input,
                    add_extension_to_output)
            self.call_when_finished(output_fname, output_base_name,
                    add_extension_to_input, add_extension_to_output)

################################################################################
# Builds a string of WorkflowTool objects based on the array of ToolInfo objects
# given as a parameter.
#
# Returns the first WorkflowTool object in the workflow. A call to this objects
# run method will call run on the next WorkflowTool object, which will call run
# on the next WorkflowTool object, and so on.
#
# The order of the workflow is based on the order of the ToolInfo objects in
# tool_infos.
#
# params:
# tool_infos - An array of ToolInfo objects that represents a workflow.
################################################################################
def build_workflow(tool_infos):
    tools = []

    #create WorkflowTool objects
    for tool_info in tool_infos:
        tools.append(WorkflowTool(tool_info))

    #set each tools call_when_finsished method to
    #be the next tools run method 
    for i in range(len(tools) - 1):
        tools[i].set_call_when_finished(tools[i + 1].run)

    return tools[0]
