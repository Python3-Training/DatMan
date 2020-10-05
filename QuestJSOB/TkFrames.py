from abc import *

from tkinter import *
from tkinter import messagebox


class TkParent(ABC):
    ''' What every parent knows '''

    @abstractmethod
    def show_error(title, message):
        ''' How to log / show an error '''
        pass

    @abstractmethod
    def form_done(self, changed, tag, dict_):
        ''' TkForm / Child Forms: Exit routine callback. '''
        pass


class TkForm(ABC):
    ''' What every child-view, has '''

    def __init__(self):
        self.title = 'Tk Form'

    @abstractmethod
    def create_form(self, root, name_tag):
        ''' Called by TkParent  '''
        pass

    @abstractmethod
    def destroy(self):
        ''' Usually called by TkParent, 
        after CHILD calls form_done() '''
        pass

    @abstractmethod
    def get_dict(self, dict_) -> bool:
        ''' Usually called by TkParent.
        Return True if the data is assigned '''
        pass

    @abstractmethod
    def put_dict(self, dict_) -> bool:
        ''' Usually called by TkParent.
        Return True if the data is able to be used '''
        pass

