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
from QuestJSOB.TkMacro import *
from QuestJSOB.Questions import Quest as Quest
from QuestJSOB.QuestExchange import EncodedJSOB

class FrmQuestBrowse(TkForm):
    ''' Data importation Form '''
    def __init__(self):
        self._parent = None
        self._data = list()
        self._frame = None
        self._name_tag = None
        self._text_item = None
        self._pw_quest = None
        self._lstbx_items = None

    def _on_browse_click(self, vevent):
        line = McListbox.get_selected(self._lstbx_items)
        if line:
            pos = line.find('\t')
            if pos == -1:
                return
            else:
                index = int(line[0:pos]) - 1
                self._pw_quest = self._data[index]
                block = str(self._pw_quest)
                McText.upl(self._text_item, block)

    def _on_share_encode(self):
        if not McText.has_text(self._text_item):
            self._parent.show_error(
                "No Data", 
                "Please select an item to encode?")
            return
        block = McText.get(self._text_item).strip()
        if EncodedJSOB.is_encoded(block):
            return
        encoded = EncodedJSOB.encode(block)
        McText.unlock(self._text_item)
        McText.put(self._text_item, encoded)
        McText.lock(self._text_item)

    def _on_share_decode(self):
        if not McText.has_text(self._text_item):
            return
        text = McText.get(self._text_item).strip()
        if not EncodedJSOB.is_encoded(text):
            self._parent.show_error(
                "Unsupported Format", 
                "Please paste an Encoded JSOB question?")
            return
        zdict = EncodedJSOB.decode(text)
        if not zdict:
            self._parent.show_error(
                "Unsuported Format", 
                "Unknown JSOB format. Time to upgrade?")
            return
        self._pw_quest = None
        try:
            data = eval(zdict)
            self._pw_quest = Quest(data)
            block = str(self._pw_quest)
            McText.upl(self._text_item, block)
            self._parent.title('JSOB Question Decoded.')
            return
        except:
            self._parent.show_error(
                "Unsuported Dictionary Format", 
                "Unsuported JSOB data. Time to upgrade?")

    def _on_share_import(self):
        if not McText.has_text(self._text_item):
            self._parent.show_error(
                "No Data", 
                "Please paste an item to import?")
            return
        self._pw_quest = None

    def _on_clip_paste(self):
        text = None
        try:
            text = self._parent.clipboard_get().strip()
        except:
            pass
        if not text:
            self._parent.show_error(
                "No Data", 
                "The clipboard is empty?")
            return
        self._pw_quest = None
        McText.upl(self._text_item, text)

    def _on_clip_copy(self):
        if not McText.has_text(self._text_item):
            self._parent.show_error(
                "No Data", 
                "Please select an item to copy to the clipboard?")
            return
        if not self._pw_quest:
            self._parent.show_error(
                "No Question", 
                "Please select a question to copy to the clipboard.")
            return
        str_ = McText.get(self._text_item).strip()
        self._parent.clipboard_clear()
        self._parent.clipboard_append(str_)
        self._parent.title(f"Copied {self._pw_quest.ID} to Clipboard")

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
        Button(zlf_sidem, text="Encode", width=10, command=self._on_share_encode).pack()
        Button(zlf_sidem, text="Decode", width=10, command=self._on_share_decode).pack()
        Button(zlf_sidem, text="Import", width=10, command=self._on_share_import).pack()
        Button(zlf_sidem, text="Copy", width=10, command=self._on_clip_copy).pack()
        Button(zlf_sidem, text="Paste", width=10, command=self._on_clip_paste).pack()

        # LabelFrame Top
        zlf_items = LabelFrame(self._frame, 
                               text=" Questions  ", 
                               bg='dark green', fg='white')

        self._lstbx_items = McListbox.create(zlf_items)
        McGrid.fill_cell(zlf_items, self._lstbx_items, 0, 0)
        self._lstbx_items.bind('<<ListboxSelect>>', self._on_browse_click)

        # LabelFrame Center
        zlf_item = LabelFrame(self._frame, text=" Quest  ",
                              bg='dark green', fg='white')

        self._text_item = Text(zlf_item, bg='light gray')
        McGrid.fill_cell(zlf_item, self._text_item, 0, 0)
        McText.lock(self._text_item)

        self._frame.add(zlf_sidem)
        self._frame.add(zlf_items)
        self._frame.add(zlf_item)
        zlf_sidem.grid(row=0, column=0, sticky=N+E)
        #McGrid.fill_cell(self._frame, zlf_sidem, 0, 0, sticky=N+E)
        zlf_items.grid(row=0, column=1, sticky=N+W)
        #McGrid.fill_cell(self._frame, zlf_items, 0, 1, sticky=N+W)
        McGrid.fill_cell(self._frame, zlf_item, 1, 1)

        self._parent.grid_columnconfigure(0, weight=1)
        self._parent.grid_rowconfigure(0, weight=1)
        self._frame.pack(anchor=CENTER, fill=BOTH, expand=True)
        return self

    def get_data(self, quest_data) -> bool:
        ''' Return: True if the data is assigned '''
        if not isinstance(quest_data, dict):
            return False
        quest_data.clear()
        quest_data.extend(self._data)
        return True

    def put_data(self, quest_data) -> bool:
        ''' Return: True if the data is able to be used '''
        if not isinstance(quest_data, list):
            return False
        if not quest_data:
            return False
        self._data.clear()
        self._data.extend(quest_data)
        short = list()
        for ss, quest in enumerate(quest_data):
            short.append(f'{str(ss+1):>04}\t {quest.question[0:80]} ...')
        McListbox.set(self._lstbx_items, short)
        return True

