import ctypes
import itertools
import win32api
from time import sleep
from tkinter.filedialog import *
from tkinter.ttk import *

import win32con

import KB_module as KB

user32 = ctypes.windll.user32


def getpath():
    return os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Main:
    def __init__(self):
        #root building
        self.root = Tk()
        self.root.title("VPP")
        #icon
        icon = resource_path('icon.ico')
        self.root.iconbitmap(icon)
        #adding menu bar
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        #File menu
        self.filemenu = Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        # "open" submenu
        self.OpenMenu = Menu(self.filemenu,tearoff=0)
        self.filemenu.add_cascade(label='Open', menu=self.OpenMenu, underline=0)
        self.OpenMenu.add_command(label="Parse", command=self.Parse)
        self.OpenMenu.add_command(label="Import", command=self.Open)


        self.filemenu.add_command(label="Save", command=self.Save)
        #info menu
        self.Info = Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label="Info", menu=self.Info)
        self.Info.add_command(label="About", command=InfoWindow)
        #Creating tabs
        self.Tabs = Notebook(self.root)
        self.Tabs.pack()
        #Adding frames to Noteboot
        self.EditTab = Frame()
        self.LibraryTab = Frame()
        self.Tabs.add(self.EditTab,text = 'Edit')
        self.Tabs.add(self.LibraryTab,text = 'Library')


        #Layout for Edit frame
        self.NotesBox = Text(self.EditTab, height=20, width=50)
        self.NotesBox.pack(side=RIGHT,expand = 1, fill= BOTH)
        self.PlayBtn = Button(self.EditTab, text='Play', command=self.Play)
        self.PlayBtn.pack(side=RIGHT)


        #Layout for Library frame
        self.LibList = Listbox(self.LibraryTab)
        self.LibList.pack(side=LEFT, fill=Y)







        self.root.mainloop()


    def Parse(self):
        """Parse raw txt file """
        file = self.OpenSheet().read()
        notes = file.split(' ')
        notes = self.Translate(notes)
        self.Insert2(notes, self.NotesBox)

    def Save(self):
        """save Note sheet"""
        name = asksaveasfile(filetypes=[("Notes", ".txt")], defaultextension=".txt")
        text2save = str(self.NotesBox.get(0.0, END))
        name.write(text2save)
        name.close

    def Open(self):
        """open Note sheet"""
        file = askopenfile(mode="r", filetypes=[("Notes", ".txt")])
        notes = file.read()
        self.NotesBox.delete(0.0, END)
        self.NotesBox.insert(0.0, notes, END)

    def Insert2(self, text, widget):
        """Insert to widget(widget) and add \n to every 10th item in list(text) """
        widget.delete(0.0, END)
        ss = ""
        t = 0
        for T in text:
            t += 1
            ss += T + " "
            if t == 10:
                t = 0
                ss += '\n'
        widget.insert(END, ss)
    def Play(self):
        """Plays song in Text widget(NotesBox) """
        if self.NotesBox.get(0.0, END) == "\n":
            self.Open()
            return
        notes = str(self.NotesBox.get(0.0, END))
        sleep(5)
        self.ActuallPlay(notes)
        return

    def ActuallPlay(self, notes):
        sheet = []
        sheetN = notes.split('\n')
        for s in itertools.chain(sheetN):
            ss = s.split(' ')
            for a in ss:
                sheet.append(a)
        while '' in sheet:
            sheet.remove('')
        for note in sheet:
            note = note.split(':')
            if win32api.GetAsyncKeyState(win32con.VK_INSERT) != 0:
                break
            KB.Press(note[0], note[1])

    def Translate(self, notes,pause = 100):
        """writing notes in note:pause style"""
        NewNotes = []
        for note in notes:
            line = note + ':' + str(pause)
            NewNotes.append(line)
        return NewNotes

    def OpenSheet(self):
        file = askopenfile(mode="r", filetypes=[("Notes", ".txt")])
        return file

class InfoWindow:
    def __init__(self):

        win = Toplevel()
        win.geometry("200x100")
        win.wm_attributes('-topmost',1)
        win.title('About')
        message = "Authors:\nRED_EYE\nVlad Bronks"
        Label(win, text=message).pack()

        Button(win, text='OK', command=win.destroy).pack()

Main()
