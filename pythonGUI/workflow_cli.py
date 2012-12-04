from tool_info import *
from workflow import *

def print_about():
    print "Team Fortnightly Workflow Tool Command Line Interface"
    print "-----------------------------------------------------"

def get_tool_infos():
    #TODO make this NOT hard coded
    tool_a_input = ToolArgInfo("input", "", "")
    tool_a_output = ToolArgInfo("output", "", "")
    tool_a = ToolInfo("python", "testTools\\a.py", tool_a_input, tool_a_output)

    tool_b_input = ToolArgInfo("input", "", "")
    tool_b_output = ToolArgInfo("output", "", "")
    tool_b = ToolInfo("python", "testTools\\b.py", tool_b_input, tool_b_output)

    tool_c_input = ToolArgInfo("input", "", "")
    tool_c_output = ToolArgInfo("output", "", "")
    tool_c = ToolInfo("python", "testTools\\c.py", tool_c_input, tool_c_output)

    return [tool_a, tool_b, tool_c]

def prompt_tool_select():
    tool_index = int(raw_input(">"))
    print "To add a tool to process the output from the last added tool enter", 
    print " 'a'."
    print "To stop adding tools to the workflow press 's'."
    loop_char = raw_input(">")
    return (tool_index, loop_char == 'a')

#script
print_about()

tool_infos = get_tool_infos()

print "available tools:"
for i in range(len(tool_infos)):
    print str(i) + " : " + tool_infos[i].command

print "\nselect the first tool in the workflow (0 - %d)" % (len(tool_infos) - 1)

selected_tools = []

loop = True
while loop:
    selected = prompt_tool_select()
    selected_tools.append(tool_infos[selected[0]])
    loop = selected[1]

print "\nnow select the input file name."
input_fname = raw_input(">")

step_tuples = build_step_tuples(selected_tools, input_fname)

print "running workflow"
print "----------------"

run_workflow(step_tuples)
