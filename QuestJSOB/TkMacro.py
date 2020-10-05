from tkinter import *

class McMenu:
    ''' Make Menu() management a tad easier.
    '''
    @staticmethod
    def enable_item(menubar, tag_name):
        menubar.entryconfig(tag_name, state="normal")

    @staticmethod
    def disable_item(menubar, tag_name):
        menubar.entryconfig(tag_name, state="disabled")

class McText:
    ''' Help the Text() work as in other platforms.
    '''
    @staticmethod
    def get(inst) -> str:
        ''' Get text from the Text() Widget '''
        return inst.get("1.0", END)

    @staticmethod
    def put(inst, text) -> None:
        ''' Copy text into the Text() Widget '''
        inst.delete('1.0', END)
        inst.insert('1.0', text)

    @staticmethod
    def clear(inst) -> None:
        ''' Remove text from the Text() Widget '''
        inst.delete('1.0', END)
