import sys
import subprocess

def default_workflow_output_handler(process):
    sys.stdout.flush()
    while True:
        next_line = process.stdout.readline()
        if not next_line:
            break
        print "\r" + next_line
        sys.stdout.flush()

class WorkflowTool:
    def __init__(self, tool_info, output_handler =
            default_workflow_output_handler):
        self.tool_info = tool_info
        self.output_handler = output_handler
        self.call_when_finished = None

    def set_call_when_finished(self, call_when_finished):
        self.call_when_finished = call_when_finished

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
