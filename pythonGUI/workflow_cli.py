import os

from tool_info import *
from workflow import *

def print_about():
    print "Team Fortnightly Workflow Tool Command Line Interface"
    print "-----------------------------------------------------"

def print_step_tuples(step_tuples):
    print step_tuples[0]
    if len(step_tuples) > 1 and step_tuples[1]:
        print_step_tuples(step_tuples[1])

def get_tool_infos():
    #TODO make this NOT hard coded

    #load in test tools
    tool_a_input = ToolArgInfo("input", "", "", ".txt")
    tool_a_output = ToolArgInfo("output", "", "", ".txt")
    tool_a = ToolInfo("python", "testTools%sa.py" % os.sep, tool_a_input,
            tool_a_output)

    tool_b_input = ToolArgInfo("input", "", "", ".txt")
    tool_b_output = ToolArgInfo("output", "", "", ".txt")
    tool_b = ToolInfo("python", "testTools%sb.py" % os.sep, tool_b_input,
            tool_b_output)

    tool_c_input = ToolArgInfo("input", "", "", ".txt")
    tool_c_output = ToolArgInfo("output", "", "", ".txt")
    tool_c = ToolInfo("python", "testTools%sc.py" % os.sep, tool_c_input,
            tool_c_output)

    #isis tools
    mro2isis_input = ToolArgInfo("from", "from=", "", ".IMG")
    mro2isis_output = ToolArgInfo("to", "to=", "", ".cub")
    mro2isis = ToolInfo("", "mroctx2isis", mro2isis_input, mro2isis_output)

    return [tool_a, tool_b, tool_c, mro2isis]
#    return [tool_a, tool_b, tool_c]

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
    new_tool = tool_infos[selected[0]]
    selected_tools.append(new_tool)
    print "\nYou have added '%s' to the workflow\n" % new_tool.command 
    loop = selected[1]

print "\nnow select the input file name."
input_fname = raw_input(">")

step_tuples = build_step_tuples(selected_tools, input_fname)

print "running workflow"
print "----------------"

#print_step_tuples(step_tuples)
run_workflow(step_tuples)