from Tkinter import *

from load_tools import get_tool_infos

# TODO: Replace the "obj" strings with ToolInfo instances
# TODO: return actual tools
# TODO: Eventually instantiate the ToolInfo objects with data from file.
def load_available_tools():
#    return [("tool A", "obj"), ("tool B", "obj"), ("tool C", "obj"),
#            ("tool D", "obj"), ("tool F", "obj")]
    tool_infos = get_tool_infos()
    tool_tuples = []
    for tool in tool_infos:
        tool_tuples.append((tool.command, tool))
    return tool_tuples

# Manages a tkinter listbox that displays tools
class ToolBox:
    def __init__(self, parent, tool_tuples = None):
        self.listbox = Listbox(parent)
        self.tool_tuples = []
        if tool_tuples:
            self.insert_tools(tool_tuples)

    def insert_tools(self, tool_tuples):
        self.tool_tuples.extend(tool_tuples)
        for tool in tool_tuples:
            self.listbox.insert(END, tool[0])

    def insert_tool(self, tool_tuple):
        self.tool_tuples.append(tool_tuple)
        self.listbox.insert(END, tool_tuple[0])

    def selected_index(self):
        selected_index = self.listbox.curselection()
        if len(selected_index) > 0:
            return int(selected_index[0])
        else:
            return -1

    def selected(self):
        index = self.selected_index()
        if index >= 0:
            return self.tool_tuples[index]
        else:
            return None

    def remove_selected(self):
        index = self.selected_index()
        if index >= 0:
            self.listbox.delete(index)
            self.tool_tuples.pop(index)

    def pack(self, **options):
        self.listbox.pack(options)

    def __str__(self):
        string = "---- ToolBox instance ----\n"
        for tool in self.tool_tuples:
            string = string + repr(tool) + "\n"
        string = string + "--------------------------"
        return string

# Adds a tool to the workflow ToolBox
def add_tool(target_tool_box, tool_tuple):
    target_tool_box.insert_tool(tool_tuple)

# instantiate the GUI
root = Tk()
root.title("ISIS Workflow GUI")

leftboxframe = Frame(root)
lLabel = Label(leftboxframe, text="Available Tools")
lLabel.pack()
toolboxL = ToolBox(leftboxframe, load_available_tools())
toolboxL.pack()
leftboxframe.pack(side=LEFT)

buttonframe = Frame(root)

moveR = Button(buttonframe, text="add >>",
        command= lambda: add_tool(toolboxR, toolboxL.selected()))
moveR.pack(fill=X)
moveL = Button(buttonframe, text="<< delete",
        command = lambda: toolboxR.remove_selected())
moveL.pack(fill=X)

buttonframe.pack(side=LEFT)

rightboxframe = Frame(root)
rLabel = Label(rightboxframe, text="Workflow")
rLabel.pack()
toolboxR = ToolBox(rightboxframe)
toolboxR.pack()
rightboxframe.pack(side=LEFT)

mainloop()
