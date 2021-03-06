#!/usr/bin/python
#import tkinter
from tkinter import *

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Centered Window")
        self.style = Style()
        self.style.theme_use("default")
        #self.centerWindow()
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit())
        quitButton.place(x=50,y=50)


    def centerWindow(self):
        w = 290
        h = 150
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = Tk()
    root.geometry("500x250+100+300")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()