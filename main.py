from tkinter import *
from subprocess import check_output
from os import getenv

def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()

class Class:
    def __init__(self, title, cmd, category):
        self.title = title
        self.cmd = cmd
        self.category = category

    def toString(self):
        return self.title + "\n" + self.cmd + "\n" + self.category

def runCmd(text):
    check_output(text, shell=False)
    root.destroy()

def buildRoot():
    clearList = root.winfo_children()

    for child in clearList:
        child.destroy()

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    catorclassremove = Menu(filemenu, tearoff=0)

    catorclassremove.add_command(label="Class", command=removeClass)
    catorclassremove.add_command(label="Category", command=removeCat)

    filemenu.add_command(label="Add", command=addClass)
    filemenu.add_cascade(label="Remove", menu=catorclassremove)

    filemenu.add_separator()

    filemenu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Report Bug", command=donothing)
    helpmenu.add_command(label="Github Repo", command=donothing)
    helpmenu.add_command(label="About", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    widgets.clear()

    for cat in categories:
        widgets.append(Label(text=cat, font='Helvetica 18 bold'))

        for c in classes:
            if (c.category == cat):
                widgets.append(Button(text=c.title, command=(lambda *args: runCmd(c.cmd))))

    for widget in widgets:
        widget.pack()

def addClass():
    add = Toplevel(root)
    add.attributes('-toolwindow', True)
    add.title("Add Class")

    label = Label(add, text="Title")
    entry = Entry(add)

    label1 = Label(add, text="Code")
    entry1 = Entry(add)

    label2 = Label(add, text="Password")
    entry2 = Entry(add)

    optFrame = Frame(add)
    label3 = Label(optFrame, text="Select Category")
    OptionList = ["New Category"] + categories
    variable = StringVar(add)
    variable.set(OptionList[0])
    oldText = "new"
    catEntry = None

    def catSelected(text):
        nonlocal catEntry
        nonlocal oldText
        if (oldText != text):
            if (text == "New Category"):
                catEntry = Entry(optFrame)
                catEntry.pack(side=BOTTOM)
            else:
                catEntry.destroy()

            oldText = text
    variable.trace("w", lambda *args: catSelected(variable.get()))
    if (variable.get() == "New Category"):
        catSelected("New Category")

    opt = OptionMenu(optFrame, variable, *OptionList)

    def exitAdd():
        add.destroy()
        add.update()

    def doneAdd():
        cmd = getenv("APPDATA")+r"\Zoom\bin\Zoom.exe --url=zoommtg://zoom.us/join?action=join&confno="+entry1.get().strip()
        if (entry2.get().strip() != ""):
            cmd += (r"&pwd=" + entry2.get().strip())

        if (variable.get() != "New Category"):
            cat = variable.get()
        else:
            cat = catEntry.get()
            categories.append(cat)

        classes.append(Class(entry.get(), cmd, cat))
        exitAdd()

        buildRoot()
        writeFile()

    buttonFrame = Frame(add)
    okAdd = Button(buttonFrame, text="Ok", command=doneAdd)
    okCancel = Button(buttonFrame, text="Cancel", command=exitAdd)

    label.pack()
    entry.pack(padx=5)

    label1.pack()
    entry1.pack(padx=5)

    label2.pack()
    entry2.pack(padx=5)

    optFrame.pack()
    label3.pack()
    opt.pack()

    buttonFrame.pack()
    okAdd.pack(side=LEFT)
    okCancel.pack(side=RIGHT)

    add.mainloop()

def removeCat():
    removeCatWin = Toplevel(root)
    removeCatWin.attributes('-toolwindow', True)
    removeCatWin.title("Remove Category")

    label = Label(removeCatWin, text="Pick Category")

    variable = StringVar(removeCatWin)
    variable.set(categories[0])
    catDropDown = OptionMenu(removeCatWin, variable, *categories)

    label1 = Label(removeCatWin, text="This will remove all classes in the category.")

    def exitRemoveCat():
        removeCatWin.destroy()
        removeCatWin.update()

    def doneRemoveCat():
        for cat in categories[:]:
            if (cat == variable.get()):
                for c in classes[:]:
                    if (c.category == cat):
                        classes.remove(c)

                categories.remove(cat)

        exitRemoveCat()
        buildRoot()
        writeFile()


    buttonFrame = Frame(removeCatWin)
    okAdd = Button(buttonFrame, text="Ok", command=doneRemoveCat)
    okCancel = Button(buttonFrame, text="Cancel", command=exitRemoveCat)

    label.pack()
    catDropDown.pack()
    label1.pack()

    buttonFrame.pack()
    okAdd.pack(side=LEFT)
    okCancel.pack(side=RIGHT)

    removeCatWin.mainloop()

def removeClass():
    removeClassWin = Toplevel(root)
    removeClassWin.attributes('-toolwindow', True)
    removeClassWin.title("Remove Class")

    label = Label(removeClassWin, text="Pick Class")

    variable = StringVar(removeClassWin)
    variable.set(classes[0].title)

    classList = list()
    for c in classes:
        classList.append(c.title)

    classDropDown = OptionMenu(removeClassWin, variable, *classList)

    def exitRemoveClass():
        removeClassWin.destroy()
        removeClassWin.update()

    def doneRemoveClass():
        for c in classes[:]:
            if (c.title == variable.get()):
                classes.remove(c)

        exitRemoveClass()
        buildRoot()
        writeFile()


    buttonFrame = Frame(removeClassWin)
    okAdd = Button(buttonFrame, text="Ok", command=doneRemoveClass)
    okCancel = Button(buttonFrame, text="Cancel", command=exitRemoveClass)

    label.pack()
    classDropDown.pack()

    buttonFrame.pack()
    okAdd.pack(side=LEFT)
    okCancel.pack(side=RIGHT)

    removeClassWin.mainloop()

def writeFile():
    f = open("webinars.dat", "w")
    for cat in categories:
        f.write(cat + "\n")

    f.write("\n")

    for c in classes:
        f.write(c.toString() + "\n")

    f.close()

def readFile():
    classRead = False

    f = open("webinars.dat", "r")

    while (True):
        inText = f.readline()
        if (inText.strip() == ""):
            if (not classRead):
                classRead = True
            else:
                break
        else:
            if (classRead):
                classes.append(Class(inText[:-1], f.readline()[:-1], f.readline()[:-1]))
            else:
                categories.append(inText[:-1])

    f.close()

categories = list()
classes = list()
widgets = list()

readFile()

root = Tk()
root.title("Webinars")
root.option_add('*Font', '19')

buildRoot()

root.mainloop()