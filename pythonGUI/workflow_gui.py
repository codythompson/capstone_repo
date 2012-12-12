from Tkinter import *

def load_available_tools():
    return ["tool A", "tool B", "tool C", "tool D", "tool F"]

class ToolBox:
    def __init__(self, root, tools=None):
        self.listbox = Listbox(root)
        if tools:
            self.insert_tools(tools)

    def insert_tools(self, tools):
        for tool in tools:
            self.listbox.insert(END, tool)

    def curselection(self):
        return self.listbox.curselection()

    def pack(self, **options):
        self.listbox.pack(options)

def print_selection(curse_whatevs):
    print curse_whatevs

root = Tk()

toolboxL = ToolBox(root, load_available_tools())
toolboxL.pack(side=LEFT)

buttonframe = Frame(root)

moveR = Button(buttonframe, text=">>",
        command= lambda: print_selection(toolboxL.curselection()))
moveR.pack()
moveL = Button(buttonframe, text="<<")
moveL.pack()

buttonframe.pack(side=LEFT)

toolboxR = ToolBox(root)
toolboxR.pack(side=LEFT)

mainloop()
