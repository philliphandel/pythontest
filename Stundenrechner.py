# -*- coding: utf-8 -*-

import datetime
import os
from tkinter import *
from pathlib import Path

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
CONFIGFILENAME = "app.config"


class Dictionary:

    def __init__(self, stdlanguage="en"):
        self.__dic = {}
        self.__stdlanguage = stdlanguage
        self.language = stdlanguage
        for lan in os.listdir("./strdic"):
            language = lan.replace(".strdic", "")
            self.__dic[language] = {}
            file = open("./strdic/" + lan, "br")
            file = file.readlines()
            for line in file:
                line = line.decode("utf8")
                if line[-1] == "\n":
                    line = line[:-1]
                if line[-1] == "\r":
                    line = line[:-1]
                line = line.split(" ", 1)
                self.__dic[language][line[0]] = line[1]

    def change_language(self, language):
        self.language = language

    def con(self, word):
        try:
            return self.__dic[self.language][word]
        except KeyError:
            return word


class App:

    def __init__(self, lan="de", pos=None):
        if pos is None:
            try:
                # C:\Users\Handel\AppData\Local\Stundenrechner
                file = open(str(Path.home()) + "\\AppData\\Local\\Stundenrechner\\" + CONFIGFILENAME, "r")
                pos = str(file.readline())
                if pos[-1] == "\n" or pos[-1] == "\r":
                    pos = pos[:-1]
            except FileNotFoundError:
                pos = "+100+100"
        self.language = lan
        self.dictionary = Dictionary(self.language)

        self.tk = Tk()
        self.tk.geometry("280x120" + pos)
        self.tk.wm_maxsize(280, 120)
        self.tk.wm_minsize(280, 120)
        self.tk.resizable(0, 0)
        self.tk.protocol("WM_DELETE_WINDOW", self.on_close)

        self.hourmenu = Menu(self.tk)
        self.hournavigationmenubar = Menu(self.hourmenu)
        self.hourmenu.add_cascade(label=self.dictionary.con("navigation"), menu=self.hournavigationmenubar)
        self.hournavigationmenubar.add_command(label=self.dictionary.con("endtimecalculator"),
                                               command=self.switch_to_end)
        self.hournavigationmenubar.add_command(label=self.dictionary.con("breaktimecalculator"),
                                               command=self.switch_to_break)
        self.hoursitemenubar = Menu(self.hourmenu)
        self.hourmenu.add_cascade(label=self.dictionary.con("site"), menu=self.hoursitemenubar)
        self.hoursitemenubar.add_command(label=self.dictionary.con("reset"), command=self.clear_fields)
        self.hoursitemenubar.add_command(label=self.dictionary.con("languagechange"), command=self.change_language)

        self.endmenu = Menu(self.tk)
        self.endnavigationmenubar = Menu(self.endmenu)
        self.endmenu.add_cascade(label=self.dictionary.con("navigation"), menu=self.endnavigationmenubar)
        self.endnavigationmenubar.add_command(label=self.dictionary.con("worktimecalculator"),
                                              command=self.switch_to_hour)
        self.endnavigationmenubar.add_command(label=self.dictionary.con("breaktimecalculator"),
                                              command=self.switch_to_break)
        self.endsitemenubar = Menu(self.endmenu)
        self.endmenu.add_cascade(label=self.dictionary.con("site"), menu=self.endsitemenubar)
        self.endsitemenubar.add_command(label=self.dictionary.con("reset"), command=self.clear_fields)
        self.endsitemenubar.add_command(label=self.dictionary.con("languagechange"), command=self.change_language)

        self.breakmenu = Menu(self.tk)
        self.breaknavigationmenubar = Menu(self.breakmenu)
        self.breakmenu.add_cascade(label=self.dictionary.con("navigation"), menu=self.breaknavigationmenubar)
        self.breaknavigationmenubar.add_command(label=self.dictionary.con("worktimecalculator"),
                                                command=self.switch_to_hour)
        self.breaknavigationmenubar.add_command(label=self.dictionary.con("endtimecalculator"),
                                                command=self.switch_to_end)
        self.breaksitemenubar = Menu(self.breakmenu)
        self.breakmenu.add_cascade(label=self.dictionary.con("site"), menu=self.breaksitemenubar)
        self.breaksitemenubar.add_command(label=self.dictionary.con("reset"), command=self.clear_fields)
        self.breaksitemenubar.add_command(label=self.dictionary.con("languagechange"), command=self.change_language)

        self.hourframe = Frame(self.tk)
        Label(self.hourframe, text=self.dictionary.con("workstart") + ":").grid(column=0, row=0)
        self.hourstartentry = Entry(self.hourframe)
        self.hourstartentry.grid(column=1, row=0)
        Label(self.hourframe, text=self.dictionary.con("workend") + ":").grid(column=0, row=1)
        self.hourendentry = Entry(self.hourframe)
        self.hourendentry.grid(column=1, row=1)
        Label(self.hourframe, text=self.dictionary.con("breaktime") + ":").grid(column=0, row=2)
        self.hourbreakentry = Entry(self.hourframe)
        self.hourbreakentry.grid(column=1, row=2)
        self.hourcalcbutton = Button(self.hourframe, text=self.dictionary.con("calculate"), command=self.calc_hour)
        self.hourcalcbutton.grid(column=1, row=3)
        self.hourvaluetextlabel = Label(self.hourframe)
        self.hourvaluetextlabel.grid(column=0, row=4)
        self.hourresultlabel = Label(self.hourframe, text="")
        self.hourresultlabel.grid(column=1, row=4)

        self.endframe = Frame(self.tk)
        Label(self.endframe, text=self.dictionary.con("workstart") + ":").grid(column=0, row=0)
        self.endstartentry = Entry(self.endframe)
        self.endstartentry.grid(column=1, row=0)
        Label(self.endframe, text=self.dictionary.con("breaktime") + ":").grid(column=0, row=1)
        self.endbreakentry = Entry(self.endframe)
        self.endbreakentry.grid(column=1, row=1)
        Label(self.endframe, text=self.dictionary.con("worktime") + ":").grid(column=0, row=2)
        self.endtimeentry = Entry(self.endframe)
        self.endtimeentry.grid(column=1, row=2)
        self.endcalcbutton = Button(self.endframe, text=self.dictionary.con("calculate"), command=self.calc_end)
        self.endcalcbutton.grid(column=1, row=3)
        self.endvaluetextlabel = Label(self.endframe)
        self.endvaluetextlabel.grid(column=0, row=4)
        self.endresultlabel = Label(self.endframe, text="")
        self.endresultlabel.grid(column=1, row=4)

        self.breakframe = Frame(self.tk)
        Label(self.breakframe, text=self.dictionary.con("breakstart") + ":").grid(column=0, row=0)
        self.breakstartentry = Entry(self.breakframe)
        self.breakstartentry.grid(column=1, row=0)
        Label(self.breakframe, text=self.dictionary.con("breakend") + ":").grid(column=0, row=1)
        self.breakendentry = Entry(self.breakframe)
        self.breakendentry.grid(column=1, row=1)
        self.breakcalcbutton = Button(self.breakframe, text=self.dictionary.con("calculate"), command=self.calc_break)
        self.breakcalcbutton.grid(column=1, row=3)
        self.breakvaluetextlabel = Label(self.breakframe)
        self.breakvaluetextlabel.grid(column=0, row=4)
        self.breakresultlabel = Label(self.breakframe, text="")
        self.breakresultlabel.grid(column=1, row=4)

        self.tk.config(menu=self.hourmenu)
        self.hourframe.pack()
        self.tk.title(self.dictionary.con("worktimecalculator"))
        self.curractive = self.hourframe
        self.tk.bind("<Return>", self.calc_hour)

        self.tk.mainloop()

    def on_close(self):
        path = str(Path.home()) + "\\AppData\\Local\\Stundenrechner"
        if not os.path.exists(path):
            os.makedirs(path)
        path += "\\" + CONFIGFILENAME
        file = open(path, "w")
        file.write("+" + str(self.tk.winfo_x()) + "+" + str(self.tk.winfo_y()))
        self.tk.destroy()

    def switch_to_hour(self):
        self.curractive.pack_forget()
        self.clear_fields()
        self.hourframe.pack()
        self.tk.title(self.dictionary.con("worktimecalculator"))
        self.tk.config(menu=self.hourmenu)
        self.curractive = self.hourframe
        self.tk.unbind("<Return>")
        self.tk.bind("<Return>", self.calc_hour)

    def switch_to_end(self):
        self.curractive.pack_forget()
        self.clear_fields()
        self.endframe.pack()
        self.tk.title(self.dictionary.con("endtimecalculator"))
        self.tk.config(menu=self.endmenu)
        self.curractive = self.endframe
        self.tk.unbind("<Return>")
        self.tk.bind("<Return>", self.calc_end)

    def switch_to_break(self):
        self.curractive.pack_forget()
        self.clear_fields()
        self.breakframe.pack()
        self.tk.title(self.dictionary.con("breaktimecalculator"))
        self.tk.config(menu=self.breakmenu)
        self.curractive = self.breakframe
        self.tk.unbind("<Return>")
        self.tk.bind("<Return>", self.calc_break)

    def change_language(self):
        menu = Menu(self.tk, tearoff=0)
        menu.add_command(label=self.dictionary.con("german"), command=lambda: self.menu_val("de"))
        menu.add_command(label=self.dictionary.con("english"), command=lambda: self.menu_val("en"))
        menu.add_command(label=self.dictionary.con("swedish"), command=lambda: self.menu_val("sve"))
        x = str(self.tk.winfo_pointerx())
        y = str(self.tk.winfo_pointery())
        menu.post(x, y)

    def menu_val(self, lan):
        # saves the window position for later use
        x = str(self.tk.winfo_x())
        y = str(self.tk.winfo_y())
        self.language = lan
        self.tk.destroy()
        self.__init__(lan=self.language, pos="+" + x + "+" + y)

    # emptys all labels and entry fields
    def clear_fields(self):
        self.hourstartentry.delete(0, END)
        self.hourbreakentry.delete(0, END)
        self.hourendentry.delete(0, END)
        self.endstartentry.delete(0, END)
        self.endbreakentry.delete(0, END)
        self.endtimeentry.delete(0, END)
        self.endtimeentry.insert(0, 8)
        self.breakstartentry.delete(0, END)
        self.breakendentry.delete(0, END)
        self.hourresultlabel['text'] = ""
        self.hourvaluetextlabel['text'] = ""
        self.breakresultlabel['text'] = ""
        self.breakvaluetextlabel['text'] = ""
        self.endresultlabel['text'] = ""
        self.endvaluetextlabel['text'] = ""

    def calc_hour(self, *args):
        del args

        startstr = self._prepare_inp(self.hourstartentry.get())
        endstr = self._prepare_inp(self.hourendentry.get())
        breakint = self.hourbreakentry.get()

        if startstr == "" or startstr == " ":
            startstr = "0"
        if endstr == "" or endstr == " ":
            endstr = "0"
        if breakint == "" or breakint == " ":
            breakint = "0"

        run1 = True
        usestr = ''
        starthours = 0
        startminutes = 0

        if ':' in startstr:
            startstr += ':'

            for char in startstr:

                if char is not ':':
                    usestr += char

                elif run1:
                    run1 = False
                    starthours = int(usestr)
                    usestr = ''

                else:
                    startminutes = int(usestr)

        else:
            starthours = int(startstr)
            startminutes = 0

        run1 = True
        usestr = ''
        endhours = 0
        endminutes = 0

        if ':' in endstr:
            endstr += ':'

            for char in endstr:
                if char is not ':':
                    usestr += char

                elif run1:
                    run1 = False
                    endhours = int(usestr)
                    usestr = ''

                else:
                    endminutes = int(usestr)

        else:
            endhours = int(endstr)
            endminutes = 0

        if ":" in breakint:
            breakhours = int(breakint[0])
            breakmin = int(breakint[2:])
            a = datetime.timedelta(0, 0, 0, 0, breakmin, breakhours, 0)

        else:
            a = datetime.timedelta(0, 0, 0, 0, int(breakint), 0, 0)

        x = datetime.timedelta(0, 0, 0, 0, startminutes, starthours, 0)
        y = datetime.timedelta(0, 0, 0, 0, endminutes, endhours, 0)
        z = y - x - a
        z = z.total_seconds()
        if z < 0:
            z = 24 * 60 * 60 - float(str(z).replace("-", ""))
        labelstring = self._beautify(z)

        self.hourvaluetextlabel['text'] = self.dictionary.con("result") + ":"
        self.hourresultlabel['text'] = labelstring

    def calc_end(self, *args):
        del args

        # get the content of the entry fields
        timestr = self._prepare_inp(self.endstartentry.get())
        breakint = self.endbreakentry.get()
        workstr = self._prepare_inp(self.endtimeentry.get())

        if timestr == "" or timestr == " ":
            timestr = "0"
        if breakint == "" or breakint == " ":
            breakint = "0"
        if workstr == "" or workstr == " ":
            workstr = "0"

        usestr = ''
        run1 = True
        timestr += ':'
        minutes = 0
        hours = 0
        workhours = 0
        workminutes = 0

        # indices over timestr to split timestr in its hours and minutes
        for char in timestr:

            if char is not ':':
                usestr += char

            elif run1:
                run1 = False
                hours = int(usestr)
                usestr = ''

            else:
                minutes = int(usestr)

        if ':' in workstr:
            usestr = ''
            run1 = True
            workstr += ":"

            # indices over workstr to split it into hours and minutes
            for char in workstr:

                if char is not ':':
                    usestr += char

                elif run1:
                    run1 = False
                    workhours = int(usestr)
                    usestr = ''

                else:
                    workminutes = int(usestr)

        else:
            workhours = int(workstr)
            workminutes = 0

        # creates the timedeltas
        if ":" in breakint:
            breakhours = int(breakint[0])
            breakmin = int(breakint[2:])

            y = datetime.timedelta(0, 0, 0, 0, breakmin, breakhours, 0)

        else:
            y = datetime.timedelta(0, 0, 0, 0, int(breakint), 0, 0)

        x = datetime.timedelta(0, 0, 0, 0, minutes, hours, 0)
        a = datetime.timedelta(0, 0, 0, 0, workminutes, workhours, 0)

        # evaluates the time and displays it
        time = x + y + a
        z = time.total_seconds()
        if z > 24 * 60 * 60:
            z = time.total_seconds() - (24 * 60 * 60)
        labelstring = self._beautify(z)

        self.endvaluetextlabel['text'] = self.dictionary.con("result") + ":"
        self.endresultlabel['text'] = labelstring

    def calc_break(self, *args):
        del args
        startstr = self._prepare_inp(self.breakstartentry.get())
        endstr = self._prepare_inp(self.breakendentry.get())

        if startstr == "" or startstr == " ":
            startstr = "0"
        if endstr == "" or endstr == " ":
            endstr = "0"

        run1 = True
        usestr = ''
        starthours = 0
        startminutes = 0

        if ':' in startstr:
            startstr += ':'

            for char in startstr:

                if char is not ':':
                    usestr += char

                elif run1:
                    run1 = False
                    starthours = int(usestr)
                    usestr = ''

                else:
                    startminutes = int(usestr)

        else:
            starthours = int(startstr)
            startminutes = 0

        run1 = True
        usestr = ''
        endhours = 0
        endminutes = 0

        if ':' in endstr:
            endstr += ':'

            for char in endstr:

                if char is not ':':
                    usestr += char

                elif run1:
                    run1 = False
                    endhours = int(usestr)
                    usestr = ''

                else:
                    endminutes = int(usestr)

        else:
            endhours = int(endstr)
            endminutes = 0

        x = datetime.timedelta(hours=starthours, minutes=startminutes)
        y = datetime.timedelta(hours=endhours, minutes=endminutes)
        j = y - x
        z = j.total_seconds()
        if z < 0:
            z = 24 * 60 * 60 - float(str(z).replace("-", ""))
        labelstring = str(int(z / 60))

        self.breakvaluetextlabel['text'] = self.dictionary.con("result") + ":"
        self.breakresultlabel['text'] = labelstring + " " + self.dictionary.con("minutes")

    @staticmethod
    def _beautify(seconds):
        minutes = seconds / 60
        hours = int(minutes / 60)
        minutes = str(int(round((minutes / 60 - hours) * 60, 0)))
        hours = str(hours)
        if len(minutes) < 2:
            minutes = "0" + minutes

        return hours + ":" + minutes

    @staticmethod
    def _prepare_inp(string):
        string = string.replace(".", ":")
        string = string.replace(",", ":")
        string = string.replace(";", ":")
        string = string.replace("-", ":")
        string = string.replace("_", ":")

        last = False
        newstring = ""
        for char in string:
            if char == ":":
                if not last:
                    newstring += char
                    last = True
            else:
                last = False
                if char in NUMBERS:
                    newstring += char

        return newstring


App()
