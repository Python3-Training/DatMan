#!/usr/bin/env python3
#
# Author: Randall Nagy
# Mission: Browse the Quest()ions - ONLY!

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

class FrmQuestBrowse(TkForm):
    ''' Data importation Form '''
    def __init__(self):
        self._parent = None
        self._fields = None
        self._frame = None
        self._name_tag = None
        self._tcontrol = None
        self._decoded = None
        self._encoded = None
        self._item_list = None

    def _on_copy(self):
        self._parent.show_error('TODO', '_on_copy()')

    def _on_hide(self):
        self._parent.show_error('TODO', '_on_hide()')

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

        # LabelFrame Sidebar
        zlf_sidem = LabelFrame(self._frame, text=" Actions   ",
                               bg='gold', fg='dark green')
        Button(zlf_sidem, text="Copy", width=10, command=self._on_copy).pack()
        Button(zlf_sidem, text="Hide", width=10, command=self._on_hide).pack()

        # LabelFrame Top
        zlf_items = LabelFrame(self._frame, 
                               text=" Questions  ", 
                               bg='dark green', fg='white')

        self._item_list = Listbox(zlf_items, height=5, width=100)
        self._item_list.grid(row=0, column=1, sticky=N+E)
        self._item_list.insert(0, '1', 'two', 'three', 'q', 'u', 'e', 's', 't',)

        # LabelFrame Center
        zlf_item = LabelFrame(self._frame, text=" Quest  ",
                              bg='dark green', fg='white')

        self._tcontrol = Text(zlf_item, bg='light gray')
        self._tcontrol.grid(row=0, column=0, sticky=N+E)
        self._tcontrol.config(state=DISABLED)

        self._frame.add(zlf_sidem)
        self._frame.add(zlf_items)
        self._frame.add(zlf_item)
        zlf_sidem.grid(row=0, column=0, sticky=N+E)
        zlf_items.grid(row=0, column=1, sticky=N+W)
        zlf_item.grid(row=1, column=1)
        self._frame.pack(anchor=N, fill=BOTH, expand=True)
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

