import json

class JSOB:
    ''' A quick-fix to enable multi-line strings for Python in J.S.O.N '''
    def __init__(self, file_name, backup=True):
        self.file = file_name
        self.backup = backup
        self.last_snap = None
        self.last_execption = None

    def snapshot(self) -> bool:
        ''' Backup the constructed file to a 'probably unique' file name. '''
        import time; import shutil
        self.last_snap = '~' + self.file + '.' + str(time.time()) + ".tmp"
        try:
            shutil.copyfile(self.file, self.last_snap)
        except Exception as ex:
            self.last_execption = ex
            return False
        self.last_execption = None
        return True

    @staticmethod
    def human_to_eval(data) -> str:
        ''' Encode a multi-line block, for eval() parsing '''
        results = ''
        if data.find('\r'):
            data = data.replace('\r\n', '\n')
        buffer = ''
        for seg in data.split('\n'):
            if seg.endswith('\\'):
                seg += '\n'
                buffer += seg
                continue
            if buffer:
                buffer += seg
                seg = buffer
                buffer = ''
            seg = seg.replace('\\\n', r'\\n')
            seg = seg.replace('\t', r'\t')
            results += seg
        return results

    @staticmethod
    def from_human_line(data) -> str:
        ''' Encode a single-line for json parsing '''
        if data.find('\r'):
            data = data.replace('\r\n', '\n')
        data = data.replace('\\\n', r'\\n')
        data = data.replace('\n', r'\n')
        data = data.replace('\t', r'\t')
        return data

    @staticmethod
    def __from_human(data) -> str:
        ''' Encode the multi-line for Python parsing '''
        if data.find('\r'):
            data = data.replace('\r\n', '\n')
        data = data.replace('\n\n', '\\n')
        data = data.replace('\t', '\\t')
        return data

    @staticmethod
    def to_human(json_string) ->str:
        ''' Decode the multi-line for HUMAN parsing '''
        json_string = json_string.replace(r"\n", "\n")
        json_string = json_string.replace(r"\t", "\t")
        json_string = json_string.replace(r"\\n", "\\n")
        return json_string

    def parse_one(self, zlines) -> dict:
        data = ''
        for ix in zlines:
            data += ix
            data += ' '
        return eval(data)

    def load_by_eval(self) -> list:
        ''' Parses one dictionary-entry, at-a-time, using eval - NOT THE JSON PARSER. '''
        self.last_execption = None
        results = []; errors = 0
        try:
            with open(self.file, encoding='utf-8') as fh:
                ignore = ('[', ']')
                zlines = list()
                buffer = ''
                for ss, line in enumerate(fh, 1):
                    if line.endswith('\\\n'):
                        buffer += line
                        continue
                    if buffer:
                        buffer += line
                        line = buffer
                        buffer = ''
                    line = JSOB.from_human_line(line.strip())
                    if line in ignore:
                        continue
                    if line[0] == '{':
                        if len(zlines) > 0:
                            try:
                                quest = self.parse_one(zlines)
                                results.append(quest)
                            except Exception as ex:
                                print('ERROR:', data)
                                print('\tCAUSE:', ex)
                                errors += 1
                        zlines.clear()
                        zlines.append(line)
                    else:
                        if line[0] == "}":
                            line = "}"
                        zlines.append(line)
                if len(zlines) > 0:
                    try:
                        quest = self.parse_one(zlines)
                        results.append(quest)
                    except Exception as ex:
                        print('ERROR:', data)
                        print('\tCAUSE:', ex)
                        errors += 1
        except Exception as ex:
            self.last_exception = ex
        return errors, results
    
    def load_by_json(self) -> str:
        ''' Reads file, converting JSON's 'human readable' multiline escapes, to inline \\n style. '''
        self.last_execption = None
        try:
            with open(self.file, encoding='utf-8') as fh:
                return self.from_human_line(fh.read())
        except Exception as ex:
            self.last_exception = ex
        return ''

    def sync(self, json_string) -> bool:
        ''' Save a file, backing-up if, and as, desired. '''
        if self.backup:
            self.snapshot()
        json_string = JSOB.from_human_line(json_string)
        try:
            with open(self.file, 'w') as fh:
                print(json_string, file=fh)
                return True
        except Exception as ex:
            self.last_exception = ex
        return False

if __name__ == '__main__':
    data = '"We have\\ \nTESTED\\\n' * 3
    encoded = JSOB.from_human_line(data)
    test1 = JSOB.to_human(encoded)
    assert(test1 == data)
