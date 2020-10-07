#!/usr/bin/env python3
#
# MISSION: Use a J.S.O.N friendly editor (like Notepad++ - Recommnded!)
# to spell-check, edit, and otherwise manage a collection of questions.
# Project @ https://github.com/Python3-Training/DatMan/tree/master/QuestJSOB
#
# 2020/10/01: Created, Randall Nagy
# 2020/10/02: New: Load by eval(), save / pretty-print via JSON.
# 2020/10/03: New: Categorized question reporting.
# 2020/10/06: New: Quest.GID for epoch 'rarifications. 

import sys
sys.path.insert(0, '.')
sys.path.insert(0, '../')

import json
from QuestJSOB.Questions import Quest as Quest

def find_questions():
    ''' Microsoft (sigh) ... am I right?'''
    import os
    results = []
    name = Quest.FILE_DEFAULT.split('/')[-1]
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file == name:
                node = root + '/' + file
                node = node.replace('\\','/')
                results.append(node)
    return results

if __name__ == '__main__': 
    ''' Demonstration: Putting it all together! '''
    files = find_questions()
    if len(files) != 1:
        for file in files:
            print(file)
        print('Visual Studio: One file, only?')
    else:
        zfile = files[0]
        data = Quest.Load(zfile)
        data = Quest.Reorder(data)
        Quest.Renum(data)
        Quest.Sync(data, zfile)

        for q in data:
            print(json.dumps(q.__dict__, indent = 3))
    
        for line in Quest.Tally(data):
            print(line)
