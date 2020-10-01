#!/usr/bin/env python3
# 2020/10/01: Created, Randall Nagy

import json

class JSOB:
    ''' A quick-fix to enable multi-line strings for Python in J.S.O.N '''
    def __init__(self, file_name, backup=True):
        self.file = file_name
        self.backup = backup
        self.last_snap = None
        self.last_execption = None

    def snapshot(self):
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

    def load(self) -> str:
        ''' Reads file, converting JSON's 'human readable' multiline escapes, to inline \\n style. '''
        self.last_execption = None
        data = ''
        try:
            with open(self.file, encoding='utf-8') as fh:
                data = fh.read()
                if data.find('\r'):
                    data = data.replace('\r\n', '\n')
                data = data.replace('\\\n', '\\n')
                data = data.replace('\t', '\\t')
        except Exception as ex:
            self.last_exception = ex
        return data

    def sync(self, json_string) -> bool:
        ''' Save a file, backing-up if, and as, desired. '''
        if self.backup:
            self.snapshot()
        json_string = json_string.replace("\\n", "\\\n")
        json_string = json_string.replace("\\t", "\t")
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
    def Load(file_name = FILE_DEFAULT):
        ''' Load a pre-existing file into a list of Quest()s '''
        results = list()
        coder = JSOB(file_name)
        data = coder.load()
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
    data = Quest.Load()
    Quest.Renum(data)
    Quest.Sync(data)
    for q in data:
        print(json.dumps(q.__dict__, indent = 3))
    
