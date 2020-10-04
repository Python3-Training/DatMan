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

from QuestJSOB.TkFrames import TkForm
from QuestJSOB.Questions import Quest as Quest

class FrmQuestImport(TkForm):
    ''' Data importation Form '''
    def __init__(self):
        self._parent = None
        self._fields = None
        self._frame = None

    def _on_import(self):
        self._parent.form_done(True,'',{})

    def _on_quit(self):
        self._parent.form_done(False,'',{})

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def create_form(self, zframe):
        ''' Creates another TkForm. Return TkForm / self. '''
        self._parent = zframe

        # Parent Frame
        self._frame = PanedWindow(zframe)
        self._frame.pack(anchor=N, fill=BOTH, expand=True)

        # Child Frame
        zLF1 = LabelFrame(self._frame, text=" Quest Block:  ")
        efn = Text(zLF1, bg='white')
        efn.grid(row=0, column=1)

        # Child Frame
        zLF2 = LabelFrame(self._frame, text=" Actions ")
        Button(zLF2, text="Import", width=10, command=self._on_import).pack()
        Button(zLF2, text="Quit", width=10, command=self._on_quit).pack()

        self._frame.add(zLF2)
        self._frame.add(zLF1)
        return self

    def get_dict(self, dict_) -> bool:
        ''' Return: True if the data is assigned '''
        if not isinstance(dict_, dict):
            return False
        dict_.update(self._fields)
        return True

    def put_dict(self, dict_) -> bool:
        ''' Return: True if the data is able to be used '''
        if not isinstance(dict_, dict):
            return False
        if len(dict_) == 0:
            return False
        self._fields.clear()
        self._fields.update(dict_)
        return True

