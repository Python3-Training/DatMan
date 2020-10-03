#!/usr/bin/env python3
#
# Author: Randall Nagy
# Mission: Create a reusable graphical user interface.
# Re-used: https://github.com/soft9000/PyDAO/blob/master/SqltDAO/main.py

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from QuestJSOB.Questions import Quest as Quest


class Main(Tk):

    PROJ_TYPE = '.json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ztitle = 'Quest 0.1'
        self.project = None
        self.zoptions = (
            ("Project",     [("New...", self._on_new),
                             ("Source...", self._on_open),
                             ("Sync...", self._on_save)]),
            ("Tools",       [("Export...", self._on_export),
                             ("Import...", self._on_import),
                             ("Report...", self._on_report)]),
            ("About",       [("About " + self.ztitle, self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.home = "."

        '''
        activeBackground, foreground, selectColor,
        activeForeground, highlightBackground, selectBackground,
        background, highlightColor, selectForeground,
        disabledForeground, insertBackground, troughColor.
        '''
        self.tk_setPalette(
                background="Light Green",# e.g. Global
                foreground="dark blue",  # e.g. Font color
                insertBackground="blue", # e.g. Entry cursor
                selectBackground="gold", # e.g. Editbox selections
                activeBackground="gold", # e.g. Menu selections
                )

    def _on_new(self):
        self.title(self.ztitle)
        self._show_view()
    
    def _on_open(self):
        self.project = askopenfilename(
            title="Open Project File",
            filetypes=[(f"{self.ztitle} Project", Main.PROJ_TYPE)]
            )
        if not self.project:
            return

        if True:
            messagebox.showerror(
                "W.I.P",
                "Unable to import " + self.project)
        else:
            self.title(self.project)
            self._show_view()

    
    def _on_save(self):
        if False:
            messagebox.showinfo(
                "Project Saved",
                "Project file saved.")
        else:
            messagebox.showerror(
                "No Data",
                "Sync Source Required.")           

    def _on_export(self):
        messagebox.showerror(
            "TODO: Export",
            "Sync Source Required.")
            
    def _on_import(self):
         messagebox.showerror(
            "TODO: Import",
            "Sync Source Required.")
         
    def _on_report(self):
        messagebox.showerror(
            "TODO: Report",
            "Sync Source Required.")

    def _on_about(self):
        messagebox.showinfo(
            self.ztitle,
            "Mode: Framework Testing")

    def _show_view(self):
        return False

    def _set_frame(self):
        zframe = Frame(self, width=600, height=400)
        zframe.pack(fill=BOTH)

    def begin(self):
        self.title(self.ztitle)
        try:
            image = PhotoImage(file="zicon.png")
            self.wm_iconphoto(self, image)
        except:
            pass
        zmain = Menu(self)
        for zsub in self.zoptions:
            zdrop = Menu(zmain, tearoff=False)
            zmain.add_cascade(label=zsub[0], menu=zdrop)
            for zz in zsub[1]:
                zdrop.add_command(label=zz[0], command=zz[1])
        self.config(menu=zmain)
        self._set_frame()
        return True

    def run(self):
        self.mainloop()
        return True

    def end(self):
        return True


if __name__ == "__main__":
    main = Main()
    try:
        if main.begin():
            main.run()
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            main.end()
        except:
            pass

