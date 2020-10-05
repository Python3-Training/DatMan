#!/usr/bin/env python3
#
# Author: Randall Nagy
# Mission: Manage the Quest()ion exportation - ONLY!

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from QuestJSOB.TkFrames import TkForm
from QuestJSOB.Questions import Quest as Quest
from QuestJSOB.QuestExchange import EncodedJSOB as Encoder

class FrmQuestExport(TkForm):
    ''' Data importation Form '''
    def __init__(self):
        self._parent = None
        self._fields = None
        self._frame = None
        self._name_tag = None
        self._tcontrol = None

    def _on_export(self):
        self._parent.form_done(True,self._name_tag,{})

    def _on_quit(self):
        self._parent.form_done(False,self._name_tag,{})

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def create_form(self, zframe, name_tag):
        ''' Creates another TkForm. Return TkForm / self. '''
        self._parent = zframe
        self._name_tag = name_tag

        # Parent Frame
        self._frame = PanedWindow(zframe)
        self._frame.pack(anchor=N, fill=BOTH, expand=True)

        # Child Frame
        zLF1 = LabelFrame(self._frame, text=" Quest Block:  ")
        self._tcontrol = Text(zLF1, bg='white')
        self._tcontrol.grid(row=0, column=1)

        # Child Frame
        zLF2 = LabelFrame(self._frame, text=" Actions ")
        Button(zLF2, text="Export", width=10, command=self._on_export).pack()
        Button(zLF2, text="Quit", width=10, command=self._on_quit).pack()

        self._frame.add(zLF2)
        self._frame.add(zLF1)
        return self

    def get_data(self, quest_data) -> bool:
        ''' Return: True if the data is assigned '''
        if not isinstance(quest_data, dict):
            return False
        quest_data.clear()
        quest_data.extend(self._fields)
        return True

    def put_data(self, quest_data) -> bool:
        ''' Return: True if the data is able to be used '''
        if not isinstance(quest_data, list):
            return False
        if not quest_data:
            return False
        self._fields = quest_data
        return True

