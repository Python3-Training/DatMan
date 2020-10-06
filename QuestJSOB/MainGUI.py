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

from QuestJSOB.TkMacro import McMenu, McText
from QuestJSOB.TkFrames import TkParent
from QuestJSOB.FrmQuestBrowse import FrmQuestBrowse
from QuestJSOB.Questions import Quest as Quest


class Main(Tk, TkParent):

    PROJ_TYPE = '.json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ztitle = 'Quest 0.1'
        self._quest_data = list()
        self._menu_main = None
        self.project    = None
        self.pw_view    = None
        self.zoptions = (
            ("Project",     [("New...", self._on_new),
                             ("Source...", self._on_open),
                             ("Sync...", self._on_save)]),
            ("Tools",       [("Report...", self._on_report)]),
            ("About",       [("About " + self.ztitle, self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.home = "."

        self.tk_setPalette(
                background="Light Green",# e.g. Global
                foreground="dark blue",  # e.g. Font color
                insertBackground="blue", # e.g. Entry cursor
                selectBackground="gold", # e.g. Editbox selections
                activeBackground="gold", # e.g. Menu selections
                )

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def disable_menu(self):
        McMenu.disable_item(self._menu_main, 'Tools')
        McMenu.disable_item(self._menu_main, 'Project')

    def enable_menu(self):
        McMenu.enable_item(self._menu_main, 'Tools')
        McMenu.enable_item(self._menu_main, 'Project')

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
        
        self._show_view()
    
    def _on_save(self):
        if False:
            messagebox.showinfo(
                "Project Saved",
                "Project file saved.")
        else:
            self.show_error("No Data", "Synchronization source required.")         

    def _on_report(self):
      dlg = Toplevel(master=self)
      dlg.title("Database Status")
      text = Text(dlg, width=50, height=12)
      McText.put(text, 'Booper')
      McText.lock(text)
      text.pack()
      Button(dlg, text="Okay", command=dlg.destroy).pack()
      dlg.grab_set() # modal
      self.wait_window(dlg)

    def _on_about(self):
        messagebox.showinfo(self.ztitle, "Mode: Framework Testing")

    def _show_view(self) -> None:
        if not os.path.exists(self.project):
            self.show_error("File not Found", "Unable to import " + self.project)
        else:
            self._quest_data = Quest.Load(self.project)
            if not self._quest_data:
                self.show_error("No Data", "Data not found in " + self.project)
                return
            self.title(self.project)
            if not self.pw_view.put_data(self._quest_data):
                self.show_error('Data Format Error', 'Unable to load questions from ' + self.project)

    def form_data(self, crud_op, name_tag, quest_data):
        print(crud_op, name_tag, repr(quest_data))

    def form_done(self, changed, tag, quest_data):
        print(changed, tag)
        if self.pw_view:
            self.pw_view.destroy()
        self._set_frame_default()

    def _set_frame_default(self):
        fact = FrmQuestBrowse()
        self.pw_view = fact.create_form(self, 'browse')
        self.pw_view.put_data(self._quest_data)
        self.enable_menu()

    def begin(self):
        self.title(self.ztitle)
        try:
            image = PhotoImage(file="zicon.png")
            self.wm_iconphoto(self, image)
        except:
            pass
        self._menu_main = Menu(self)
        for zsub in self.zoptions:
            zdrop = Menu(self._menu_main, tearoff=False)
            self._menu_main.add_cascade(label=zsub[0], menu=zdrop)
            for zz in zsub[1]:
                zdrop.add_command(label=zz[0], command=zz[1])
        self.config(menu=self._menu_main)
        self._set_frame_default()
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

