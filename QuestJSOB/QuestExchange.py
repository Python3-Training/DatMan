
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

if __name__ == '__main__':
    test1 = 'This is\n?\ta\n?\rTEsT!' * 10
    block = EncodedJSOB.encode(test1)
    print(block)
    result1 = EncodedJSOB.decode(block)
    assert(test1 == result1)
    print('Testing success.')
