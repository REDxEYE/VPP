import os
from time import sleep
from tkinter.filedialog import *
import KB_module as KB
from tkinter.ttk import *
import tkinter.ttk as ttk
import threading
import itertools


def getpath():
    return os.path.dirname(os.path.abspath(__file__))

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title("VPP")


        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Parse", command=self.Parse)
        self.filemenu.add_command(label="Open", command=self.Open)
        self.filemenu.add_command(label="Save", command=self.Save)

        self.NotesBox = Text(self.root,height=20, width=80)
        self.NotesBox.pack(side = RIGHT)

        self.PlayBtn = Button(self.root,text = 'Play',command = self.Play)
        self.PlayBtn.pack(side = RIGHT)

        self.root.mainloop()
    def Parse(self):
        file = self.OpenSheet().read()
        notes = file.split(' ')
        notes = self.Translate(notes)
        self.Insert2(notes,self.NotesBox)
    def Save(self):
        name =  asksaveasfile(filetypes=[("Notes",".txt")])
        name+='.txt'
        text2save=str(self.NotesBox.get(0.0,END))
        name.write(text2save)
        name.close
    def Open(self):
        file = askopenfile(mode= "r",filetypes=[("Notes",".txt")])
        notes = file.read()
        self.NotesBox.delete(0.0,END)
        self.NotesBox.insert(0.0,notes,END)
    def Insert2(self,text,widget):
        widget.delete(0.0,END)
        ss = ""
        t= 0
        for T in text:
            t+=1
            ss+= T+" "
            if t == 10:
                t=0
                ss+='\n'
        widget.insert(END,ss)
    def Play(self):

        if self.NotesBox.get(0.0,END) =="\n":
            self.Open()
            return
        notes = str(self.NotesBox.get(0.0,END))
        notes.rstrip("\n")
        sheet = []

        sheetN = notes.split('\n')
        for s in itertools.chain(sheetN):
            ss = s.split(' ')
            for a in ss:
                sheet.append(a)
        while '' in sheet:
            sheet.remove('')
        sleep(2)
        self.PlayThrd = threading.Thread(target=self.ActuallPlay,args=(sheet))
        self.PlayThrd.start()
        self.StopThrd = threading.Thread(target=self.Stop)
        return
    def ActuallPlay(self,sheet):
        for note in sheet:
            note = note.split(':')
            KB.Press(note[0],note[1])
    def Stop(self):

    def Translate(self,notes):
        NewNotes = []
        for note in notes:
            line = note +':'+ str(100)
            NewNotes.append(line)
        return NewNotes

    def OpenSheet(self):
        file = askopenfile(mode = "r",filetypes=[("Notes",".txt")])
        return file
Main()