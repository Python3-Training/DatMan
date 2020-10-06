from QuestJSOB.Questions import Quest
from QuestJSOB.JSOB import JSOB

class EncodedJSOB:
    ''' Rather than fight whitespaces (etc.) here is
    an easier way to encode, and to exchange, JSOB blocks.'''
    
    @staticmethod 
    def is_encoded(message):
        for char in '$|0y':
            if message.find(char) == -1:
                return False
        return True

    @staticmethod
    def to_share(quest_obj):
        ''' Copy-out object to the human-sharable format. '''
        if not isinstance(quest_obj, Quest):
            return False
        clear = str(quest_obj)
        data = JSOB.to_human(clear)
        return EncodedJSOB.encode(data)

    @staticmethod
    def from_share(block):
        ''' Copy-in the human to_share(), to an object. '''
        data = EncodedJSOB.decode(block)
        try:
            data = JSOB.human_to_eval(data)
            return Quest(eval(data))
        except:
            pass
        return None

    @staticmethod 
    def encode(block):
        result = '\nBEGIN_BLOCK$\n'
        for ss, ch in enumerate(block,1):
            result += f'0y{ord(ch)}'
            if ss % 15 == 0:
                result += '$'
            else:
                result += '|'
        result += '\n$END_BLOCK\n'
        return result

    @staticmethod 
    def decode(jsob):
        result = ''
        rows = jsob.split('$')
        for row in rows:
            cells = row.strip().split('|')
            for cell in cells:
                if cell.startswith('0y'):
                    num = int(cell[2:])
                    result += chr(num)
        return result

