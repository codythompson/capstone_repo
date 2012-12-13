import os
import threading
from Tkinter import *

from load_tools import get_tool_infos
from workflow import *

def load_available_tools():
    tool_infos = get_tool_infos()
    tool_tuples = []
    for tool in tool_infos:
        tool_tuples.append((tool.command, tool))
    return tool_tuples

# Manages a tkinter listbox that displays tools
class ToolBox:
    def __init__(self, parent, tool_tuples = None):
        self.frame = Frame(parent)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)

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

    def get_all_tool_info(self):
        tool_infos = []
        for tool in self.tool_tuples:
            tool_infos.append(tool[1])
        return tool_infos

    def pack(self, **options):
        self.frame.pack(options)

    def __str__(self):
        string = "---- ToolBox instance ----\n"
        for tool in self.tool_tuples:
            string = string + repr(tool) + "\n"
        string = string + "--------------------------"
        return string

class RunThread(threading.Thread):
    def __init__(self, start_tool, input_file_path, output_base_name,
            callback_function):
        self.start_tool = start_tool
        self.input_file_path = input_file_path
        self.output_base_name = output_base_name
        threading.Thread.__init__(self)
    
    def run(self):
        self.start_tool.run(self.input_file_path,
            self.output_base_name)

    def stop(self):
        self.join()
        callback_function()

class RunBoxOutputHandler:
    def __init__(self, add_line_method):
        self.add_line_method = add_line_method

    def handle_output(self, next_line):
        self.add_line_method(next_line)
        print next_line

class RunBox:
    def __init__(self, parent, get_tool_info_function):
        self.frame = Frame(parent)

        self.input_entry_label = Label(self.frame, text="Input File Path:")
        self.input_entry_label.pack(fill=X)
        self.input_entry = Entry(self.frame)
        self.input_entry.pack(fill=X)

        self.outputbox_label = Label(self.frame, text="Output")
        self.outputbox_label.pack(fill=X)
        self.outputbox = Listbox(self.frame)
        self.outputbox.pack(fill=X)

        buttonframe = Frame(self.frame)
        self.runbutton = Button(buttonframe, text="Run Workflow",
                command=self.run)
        self.clearbutton = Button(buttonframe, text="Clear Output",
                command=self.clear)
        self.runbutton.pack(side=RIGHT)
        self.clearbutton.pack(side=LEFT)
        buttonframe.pack(fill=X)

        self.use_threading_checked = IntVar()
        self.use_threading = Checkbutton(self.frame, text="Run on a new thread",
                variable=self.use_threading_checked)
        self.use_threading.pack(side=RIGHT)
        if os.sep != '\\':
            self.use_threading.config(state=DISABLED)

        self.get_tool_info_function = get_tool_info_function

    def lock_run_button(self):
        self.runbutton.config(state=DISABLED)

    def unlock_run_button(self):
        self.runbutton.config(state=NORMAL)

    def run(self):
        tool_infos = self.get_tool_info_function()
        output_handler = RunBoxOutputHandler(self.add_line)
        start_tool = build_workflow(tool_infos, output_handler.handle_output,
                self.unlock_run_button)
        input_file_path = self.input_entry.get()

        if self.use_threading_checked.get() == 1:
            self.lock_run_button()
            thread = RunThread(start_tool, input_file_path, "gui_out",
                self.unlock_run_button)
            thread.start()
        else:
            start_tool.run(input_file_path, "gui_out")

    def add_line(self, line):
        self.outputbox.insert(END, line)

    def clear(self):
        self.outputbox.delete(0, END)

    def pack(self, **options):
        self.frame.pack(options)

# Adds a tool to the workflow ToolBox
def add_tool(target_tool_box, tool_tuple):
    target_tool_box.insert_tool(tool_tuple)


################################################################################
# builds the GUI
################################################################################
root = Tk()
root.title("ISIS Workflow GUI")

#toolboxes
toolframe = Frame(root)

leftboxframe = Frame(toolframe)
lLabel = Label(leftboxframe, text="Available Tools")
lLabel.pack()
toolboxL = ToolBox(leftboxframe, load_available_tools())
toolboxL.pack(side=LEFT)
leftboxframe.pack(side=LEFT)

buttonframe = Frame(toolframe)

moveR = Button(buttonframe, text="add >>",
        command= lambda: add_tool(toolboxR, toolboxL.selected()))
moveR.pack(fill=X)
moveL = Button(buttonframe, text="<< delete",
        command = lambda: toolboxR.remove_selected())
moveL.pack(fill=X)

buttonframe.pack(side=LEFT)

rightboxframe = Frame(toolframe)
rLabel = Label(rightboxframe, text="Workflow")
rLabel.pack()
toolboxR = ToolBox(rightboxframe)
toolboxR.pack()
rightboxframe.pack(side=LEFT)

toolframe.pack()

#runbox
def test_func(runbox_instance):
    runbox_instance.add_line("Testing ----------- Testing")

runbox = RunBox(root, toolboxR.get_all_tool_info)
runbox.pack(fill=X)

mainloop()
