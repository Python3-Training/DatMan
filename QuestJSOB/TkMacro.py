
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
