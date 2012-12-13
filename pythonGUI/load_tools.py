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
    #TODO make this set by user input
    spice_init.other_args.append("web=yes")

    ctxcal_input = ToolArgInfo("from", "from=", "", ".cub")
    ctxcal_output = ToolArgInfo("to", "to=", "", ".lev1.cub")
    ctxcal = ToolInfo("", "ctxcal", ctxcal_input, ctxcal_output)

    ctxevenodd_input = ToolArgInfo("from", "from=", "", ".lev1.cub")
    ctxevenodd_output = ToolArgInfo("to", "to=", "", ".lev1eo.cub")
    ctxevenodd = ToolInfo("", "ctxevenodd", ctxevenodd_input, ctxevenodd_output)

    cam2map_input = ToolArgInfo("from", "from=", "", ".lev1eo.cub")
    cam2map_output = ToolArgInfo("to", "to=", "", ".lev2.cub")
    cam2map = ToolInfo("", "cam2map", cam2map_input, cam2map_output)
    #TODO make this set by user input
    cam2map.other_args.append("map=testTools/testData/simp0.map")

    isis2std_input = ToolArgInfo("from", "from=", "", ".lev2.cub")
    isis2std_output = ToolArgInfo("from", "to=", "", ".jp2")
    isis2std = ToolInfo("", "isis2std", isis2std_input, isis2std_output)
    isis2std.other_args.append("format=jp2")

    return [tool_a, tool_b, tool_c, tool_d, mro2isis, spice_init, ctxcal,
            ctxevenodd, cam2map, isis2std]
