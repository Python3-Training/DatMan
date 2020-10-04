import abc as ABC

from tkinter import *
from tkinter import messagebox

class TkParent(ABC.ABC):
    ''' What every parent knows '''
    @ABC.abstractmethod
    def form_done(self, changed, tag, dict_):
        ''' TkForm / Child Forms: Exit routine callback. '''
        pass


class TkForm(ABC.ABC):
    ''' What every child-view, has '''
    def __init__(self):
        self.title = 'Tk Form'

    @ABC.abstractmethod
    def create_form(self, root):
        ''' Called by TkParent  '''
        pass

    @ABC.abstractmethod
    def destroy(self):
        ''' Usually called by TkParent, 
        after CHILD calls form_done() '''
        pass

    @ABC.abstractmethod
    def get_dict(self, dict_) -> bool:
        ''' Usually called by TkParent.
        Return True if the data is assigned '''
        pass

    @ABC.abstractmethod
    def put_dict(self, dict_) -> bool:
        ''' Usually called by TkParent.
        Return True if the data is able to be used '''
        pass

