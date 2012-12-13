import os

from tool_info import *

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

    #isis tools
    mro2isis_input = ToolArgInfo("from", "from=", "", ".IMG")
    mro2isis_output = ToolArgInfo("to", "to=", "", ".cub")
    mro2isis = ToolInfo("", "mroctx2isis", mro2isis_input, mro2isis_output)

    spice_init_input = ToolArgInfo("from", "from=", "", ".cub")
    spice_init = ToolInfo("", "spiceinit", spice_init_input, None)
    spice_init.other_args.append("web=yes")

    return [tool_a, tool_b, tool_c, tool_d, mro2isis, spice_init]
