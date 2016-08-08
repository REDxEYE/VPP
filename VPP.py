import ctypes
import itertools
import win32api
from time import sleep
from tkinter.filedialog import *
from tkinter.ttk import *
import json
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
        base_path = getpath()
        #base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Main:
    def __init__(self):

        #root building
        self.root = Tk()
        self.LoadLibrary()
        self.root.bind_class('Entry','<Control-v>',self.ClipBoard)
        self.root.bind_class('Entry','<Control-c>',self.copy)
        self.root.bind_class('Text','<Control-v>',self.ClipBoard)
        self.root.bind_class('Text','<Control-c>',self.copy)
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
        self.Tabs.pack(expand = 1, fill= BOTH)
        #Adding frames to Noteboot
        self.EditTab = Frame()
        self.LibraryTab = Frame()
        self.Tabs.add(self.EditTab,text = 'Edit')
        self.Tabs.add(self.LibraryTab,text = 'Library')


        #Layout for Edit frame
        self.NotesBox = Text(self.EditTab, height=20, width=50)
        self.NotesBox.pack(side=RIGHT,expand = 1, fill= BOTH)
        self.Add2LibBtn = Button(self.EditTab,text = "Add to\nlibrary",command =self.Add2lib_Window)
        self.Add2LibBtn.pack()
        self.PlayBtn = Button(self.EditTab, text='Play', command=self.Play)
        self.PlayBtn.pack(side=RIGHT)


        #Layout for Library frame
        self.LibList = Listbox(self.LibraryTab)
        self.LibList.pack(side=LEFT, fill=Y)
        self.FillLibList()

        self.PreviewFrame  = Frame(self.LibraryTab)
        self.PreviewFrame.pack(side = LEFT,expand = 1,fill = BOTH)
        self.BTNFrame  = Frame(self.PreviewFrame)
        self.BTNFrame.pack(fill = X)
        self.SaveBtn = Button(self.BTNFrame)
        self.SaveBtn.pack(side = LEFT)
        self.PlayBtn2 = Button(self.BTNFrame,text = 'Play')
        self.PlayBtn2.bind('<Button-1>',lambda _:self.Play(self.PreviewBox.get(0.0,END)))
        self.PlayBtn2.pack(side = LEFT)


        #self.LibList.bind('<Button-1>',lambda _:self.Insert2(self.Lib[self.LibList.curselection()]))
        self.LibList.bind('<<ListboxSelect>>',lambda _:self.Preview(self.LibList))
        self.PreviewBox = Text(self.PreviewFrame)
        self.PreviewBox.pack(side = LEFT,expand = 1, fill= BOTH)







        self.root.mainloop()
    def FillLibList(self):
        self.LibList.delete(0,END)
        for name in self.Lib.keys():
            self.LibList.insert(END,name)
    def ClipBoard(self,event):
        w = event.widget
        w.insert(0.0,self.root.clipboard_get())
    def copy(self, event):
        w = event.widget
        w.clipboard_clear()
        text = w.get("sel.first", "sel.last")
        w.clipboard_append(text)
    def Preview(self,List):
        index = int(List.curselection()[0])
        self.PreviewBox.delete(0.0,END)
        self.PreviewBox.insert(END,' '.join(self.Lib[List.get(index)]))
        print(self.Lib[List.get(index)])
    def Add2lib_Window(self):
        win  = Toplevel()
        win.geometry("200x100")
        win.title('Add to library')
        Label(win, text="Name").pack(side = RIGHT)
        self.Name = Entry(win)
        self.Name.pack(side = RIGHT)
        tt = Button(win, text='add')
        tt.pack(side = RIGHT)
        tt.bind('<Button-1>',lambda _:self.Add2lib_Event(self.Name.get(),win))
    def Add2lib_Event(self,Name,win):
        self.FillLibList()
        win.destroy()
        self.Lib[Name] = self.notes
        self.SaveLibrary()
    def LoadLibrary(self):
        self.path = getpath()
        is_exist = True
        try:
            _ =open(self.path + '/lib.json', 'r')
        except:
            print('lib is not found')
            is_exist = False
        if is_exist:
            print('lib is found')
            with open(self.path + '/lib.json', 'r') as libS:
                    self.Lib = json.load(libS)
        else:

            self.Lib = {}
            with open(self.path + '/lib.json', 'w') as libS:
                json.dump(self.Lib, libS)
            with open(self.path + '/lib.json', 'r') as libS:
                self.Lib = json.load(libS)
    def SaveLibrary(self):
        with open(self.path + '/lib.json', 'w') as libS:
                json.dump(self.Lib, libS)

    def Parse(self,file = None):
        """Parse raw txt file """
        if file ==None:
            file = self.OpenSheet().read()
        self.notes = file.split(' ')
        self.notes = self.Translate(self.notes)
        self.Insert2(self.notes, self.NotesBox)

    def Save(self):
        """save Note sheet"""
        name = asksaveasfile(filetypes=[("Notes", ".txt")], defaultextension=".txt")
        text2save = str(self.NotesBox.get(0.0, END))
        name.write(text2save)
        name.close

    def Open(self):
        """open Note sheet"""
        file = askopenfile(mode="r", filetypes=[("Notes", ".txt")])
        self.notes = file.read()
        self.NotesBox.delete(0.0, END)
        self.NotesBox.insert(0.0, self.notes, END)

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
    def Play(self,notes = None):
        """Plays song in Text widget(NotesBox) """
        if notes == None:
            if self.NotesBox.get(0.0, END) == "\n":
                self.Open()
                return
            notes = str(self.NotesBox.get(0.0, END))
            if not ":" in notes:
                self.Parse(notes)
                notes = str(self.NotesBox.get(0.0, END))
                return


        sleep(5)
        self.ActuallPlay(notes)
        return

    def ActuallPlay(self, notes):
        if 'list' not in str(type(notes)):
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
        else:
            for note in notes:
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
    def __init__(self,msg = None):

        win = Toplevel()
        win.geometry("200x100")
        win.wm_attributes('-topmost',1)
        win.title('About')
        if msg ==None:
            msg = "Authors:\nRED_EYE\nVlad Bronks"
        Label(win, text=msg).pack()

        Button(win, text='OK', command=win.destroy).pack()

Main()
