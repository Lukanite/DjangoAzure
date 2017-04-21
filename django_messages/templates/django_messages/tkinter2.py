from tkinter import *

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello"
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "right"}, expand=1)

        self.entry = Entry()
        self.entry.pack()
        self.contents = StringVar()
        self.contents.set("This is a variable")
        self.entry["textvariable"] = self.contents

        self.entry.bind('<Key-Return>', self.print_contents)

    def print_contents(self, event):
        print("hi. contents of entry si now ", self.contents.get())

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()