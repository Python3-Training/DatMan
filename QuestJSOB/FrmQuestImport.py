#!/usr/bin/env python3
#
# Author: Randall Nagy
# Mission: Manage the Quest()ion importation, ONLY!

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from QuestJSOB.TkFrames import TkForm
from QuestJSOB.TkMacro import McText
from QuestJSOB.Questions import Quest as Quest
from QuestJSOB.QuestExchange import EncodedJSOB as Decoder

class FrmQuestImport(TkForm):
    ''' Data importation Form '''
    def __init__(self):
        self._parent = None
        self._fields = None
        self._frame = None
        self._name_tag = None
        self._tcontrol = None
        self._decoded = None
        self._encoded = None

    def _on_import(self):
        self._parent.form_done(True,self._name_tag,{})

    def _on_decode(self):
        block = McText.get(self._tcontrol).strip()
        if Decoder.is_encoded(block):
            self._encoded = block
            self._decoded = Decoder.decode(block)
            McText.put(self._tcontrol, self._decoded)
        else:
            self._parent.show_error('Error', 'Encoded block, not found.')

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
        Button(zLF2, text="Import", width=10, command=self._on_import).pack()
        Button(zLF2, text="Decode", width=10, command=self._on_decode).pack()
        Button(zLF2, text="Quit", width=10, command=self._on_quit).pack()

        self._frame.add(zLF2)
        self._frame.add(zLF1)
        return self

    def get_data(self, quest_data) -> bool:
        ''' Return: True if the data is assigned '''
        if not isinstance(quest_data, list):
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
        self._fields.clear()
        self._fields.extend(quest_data)
        return True

