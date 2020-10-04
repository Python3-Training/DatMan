import abc as ABC

from tkinter import *
from tkinter import messagebox

class TkParent(ABC.ABC):
    ''' What every parent knows '''
    @ABC.abstractmethod
    def form_done(self, changed, tag, dict_):
        pass


class TkForm(ABC.ABC):
    ''' What every child-view, has '''
    def __init__(self):
        self.title = 'Tk Form'

    @ABC.abstractmethod
    def create_form(self, root):
        pass

    @ABC.abstractmethod
    def destroy(self):
        pass

    @ABC.abstractmethod
    def get_dict(self, dict_) -> bool:
        ''' True if the data is assigned '''
        pass

    @ABC.abstractmethod
    def put_dict(self, dict_) -> bool:
        ''' True if the data is able to be used '''
        pass


class QuestImport(TkForm):
    ''' Data importation form '''
    def __init__(self):
        self._parent = None
        self._fields = None
        self.quest_block = StringVar()
        self._frame = None

    def _on_import(self):
        self._parent.form_done(True,'',{})

    def _on_quit(self):
        self._parent.form_done(False,'',{})

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def create_form(self, zframe):
        ''' Prepares the frame for table management / creation during object initialization. '''
        self._parent = zframe

        # Parent Frame
        self._frame = PanedWindow(zframe)
        self._frame.pack(anchor=N, fill=BOTH, expand=True)

        # Child Frame
        zLF1 = LabelFrame(self._frame, text=" Quest Block:  ")
        efn = Text(zLF1, bg='white') # textvariable=self.quest_block)
        efn.grid(row=0, column=1)

        # Child Frame
        zLF2 = LabelFrame(self._frame, text=" Actions ")
        Button(zLF2, text="Import", width=10, command=self._on_import).pack()
        Button(zLF2, text="Quit", width=10, command=self._on_quit).pack()

        self._frame.add(zLF2)
        self._frame.add(zLF1)
        return self

    def get_dict(self, dict_) -> bool:
        ''' True if the data is assigned '''
        if not isinstance(dict_, dict):
            return False
        dict_.update(self._fields)
        return True

    def put_dict(self, dict_) -> bool:
        ''' True if the data is able to be used '''
        if not isinstance(dict_, dict):
            return False
        if len(dict_) == 0:
            return False
        self._fields.clear()
        self._fields.update(dict_)
        return True

