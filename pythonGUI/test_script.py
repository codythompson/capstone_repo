import os

from tool_info import *
from workflow import *

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

    tool_d_input = ToolArgInfo("input", "", "", "txt")
    tool_d = ToolInfo("python", "testTools%sd.py" % os.sep, tool_c_input, None)

#    return [tool_a, tool_b, tool_c]
#    return [tool_a, tool_b]
#    return [tool_a]
    return [tool_a, tool_d, tool_b, tool_c]

#def build_workflow(tool_infos):
#    tools = []
#
#    #create WorkflowTool objects
#    for tool_info in tool_infos:
#        tools.append(WorkflowTool(tool_info))
#
#    #set each tools call_when_finsished method to
#    #be the next tools run method 
#    for i in range(len(tools) - 1):
#        tools[i].set_call_when_finished(tools[i + 1].run)
#
#    return tools[0]
 
print "Running a->b->c"
print "==============="

start_tool = build_workflow(get_tool_infos())
start_tool.run("testTools%sout%sorig.text" % (os.sep, os.sep), "output")
