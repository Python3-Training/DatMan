#!/usr/bin/env python3
# License: MIT
# File: MyJSON (Adv02.py)
# Mission: Rename + migrate over to the MyData Module, supporting the next academic demonstration.
# Author: Randall Nagy
# Version: 1.0

import os
import os.path
import json

def create_filename(key):
    return f"{key.lower()}.json"


def base_name(file):
    return f'Record: {file.replace(".json", "")}'


def should_delete(file):
    return input(f"Delete existing '{file}'? [Y/N] ") == 'Y'


def list_files():
    results = []
    for file in os.listdir("."):
        if not file.endswith(".json"):
            continue
        results.append(file)
    return results


def create():
    # NOTE: OrderedDict best before 3.7
    record = {
        "Name":None, "Address":None, "Phone":None,
        }
    # NOTE: F-Strings as of 3.6
    for key in record:
        record[key] = input(f"Enter {key}: ")
    file = create_filename(record['Name'])
    if os.path.exists(file) and not should_delete(file):
        return False
    with open(file, "w") as fh:
        json.dump(record, fh)
    return True


def read():
    ''' Scenario: 
    User selects name to load.
    Returns data for same, else None.
    '''
    name = input("Enter Name: ")
    file = create_filename(name)
    if not os.path.exists(file):
        print(f"File '{file}' not found.")
        return None
    with open(file) as fh:
        record = json.load(fh)
        if record:
            print(record)
            return record
    return None


def update():
    ''' Scenario:
    User selects & update a record.
    Returns True if updated, else False
    '''
    record = read()
    if record:
        changed = False
        for key in record:
            print(record[key])
            value = input("Update: (enter to keep): ")
            if value:
                record[key] = value
                changed = True
    if not changed:
        return False
    file = create_filename(record['Name'])
    with open(file, "w") as fh:
        json.dump(record, fh)
    return True


def delete():
    ''' Scenario:
    User selects record to delete.
    Always returns None
    '''
    record = read()
    if record:
        file = create_filename(record['Name'])
        if should_delete(file):
            os.unlink(file)


def search():
    ''' Scenario:
    User searches for a string, in all records.
    Results are displayed.
    Returns number of occurrences found.
    Returns 0 on error, or nothing was found.
    '''
    search = input("Locate: ")
    count = 0
    if search:
        for file in list_files():
            with open(file) as fh:
                record = json.load(fh)
                if not record:
                    continue
                for key in record:
                    if record[key].find(search) != -1:
                        report = base_name(file)
                        print(report, 
                              record[key], sep='\t')
                        count += 1
    return count


def listf():
    ''' Scenario:
    Display the key (file) names, if any.
    Always returns None.
    '''
    for file in list_files():
        print("\t", base_name(file))


if __name__ == '__main__':
    options = {
        'c':create, 'r':read, 'u':update, 'd':delete,
        'l':listf, 's':search, 'q':quit
        }
    while True:
        op = input("Option: ")
        if op in options:
            options[op]()
        else:
            print("Invalid option. Try again?")
