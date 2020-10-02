#!/usr/bin/env python3
# 2020/10/01: Created, Randall Nagy
# 2020/10/02: New: Load by eval(), save / pretty-print via JSON.

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

    def normalize(self, data):
        ''' Encode the multi-line for Python parsing '''
        if data.find('\r'):
            data = data.replace('\r\n', '\n')
        data = data.replace('\n\n', '\\n')
        data = data.replace('\t', '\\t')
        return data

    def decode(self, json_string):
        ''' Decode the multi-line for HUMAN parsing '''
        json_string = json_string.replace("\\n", "\\\n")
        json_string = json_string.replace("\\t", "\t")
        return json_string.replace("\\\\ ", "\\\n\t")

    def load_by_eval(self) -> list:
        ''' Parses one dictionary-entry, at-a-time, using eval - NOT THE JSON PARSER. '''
        self.last_execption = None
        results = []; errors = 0
        try:
            with open(self.file, encoding='utf-8') as fh:
                ignore = ('[', ']')
                zlines = list()
                for ss, line in enumerate(fh, 1):
                    line = self.normalize(line.strip())
                    if line in ignore:
                        continue
                    if line[0] == '{':
                        if len(zlines) > 0:
                            try:
                                data = ''
                                for ix in zlines:
                                    data += ix
                                    data += ' '
                                zdict = eval(data)
                                results.append(zdict)
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

        except Exception as ex:
            self.last_exception = ex
        return errors, results
    
    def load_by_json(self) -> str:
        ''' Reads file, converting JSON's 'human readable' multiline escapes, to inline \\n style. '''
        self.last_execption = None
        try:
            with open(self.file, encoding='utf-8') as fh:
                return self.normalize(fh.read())
        except Exception as ex:
            self.last_exception = ex
        return ''

    def sync(self, json_string) -> bool:
        ''' Save a file, backing-up if, and as, desired. '''
        if self.backup:
            self.snapshot()
        json_string = self.decode(json_string)
        try:
            with open(self.file, 'w') as fh:
                print(json_string, file=fh)
                return True
        except Exception as ex:
            self.last_exception = ex
        return False


class Quest:
    ''' Demonstrate how to use a basic JSON-serialized dictionary. '''
    
    FILE_DEFAULT = 'AllQuestions.json'
    
    def __init__(self, vals):
        ''' Assign a QUESTion dictionary for future use. '''
        self.ID         = vals['ID']
        self.KID        = vals['KID']
        self.difficulty = vals['difficulty']
        self.association= vals['association']
        self.status     = vals['status']
        self.question   = vals['question']
        self.answer     = vals['answer']

    @staticmethod
    def Load(file_name = FILE_DEFAULT, use_eval=True):
        ''' Load a pre-existing file into a list of Quest()s '''
        results = list()
        coder = JSOB(file_name)
        if use_eval:
            errors, data = coder.load_by_eval()
            if errors:
                raise Exception(f"eval: {errors} errors were found.")
            for dict_ in data:
                results.append(Quest(dict_))
        else:
            data = coder.load_by_json()
            for zdict in json.loads(data, encoding='utf-8'):
                results.append(Quest(zdict))
        return results
        
    @staticmethod
    def Renum(values):
        ''' Demonstrate how do work on a list of Quest()ions '''
        for ss, q in enumerate(values, 1):
            q.ID = ss
        return len(values)
        
    @staticmethod
    def Sync(values, file_name = FILE_DEFAULT):
        ''' Save the data to a multi-line / human editable J.S.O.N database '''
        zlist = list()
        for obj in values:
            zlist.append(obj.__dict__)
        coder = JSOB(file_name)
        data = json.dumps(zlist, indent=3)
        return coder.sync(data)
        
    @staticmethod
    def Source():
        ''' Get a data-source that can be used by the constructor '''
        return {
            'ID'            : -1,
            'KID'           : 'tbd',
            'difficulty'    : 'undefined',
            'association'   : 'tbd',
            'status'        : 'undefined',
            'question'      : 'undefined',
            'answer'        : 'undefined'
            }

if __name__ == '__main__':
    ''' Demonstration: Putting it all together! '''
    data = Quest.Load(Quest.FILE_DEFAULT)
    Quest.Renum(data)
    Quest.Sync(data)
    for q in data:
        print(json.dumps(q.__dict__, indent = 3))
    
