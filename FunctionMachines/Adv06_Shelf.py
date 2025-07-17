#!/usr/bin/env python3
# Meta:
#region
# License: MIT
# File: Adv06_Shelf.py
# Mission: Use S3D2 to mange 'objects' on a 'shelf'
# Related: https://github.com/Python3-Training/DatMan
# Source:  https://github.com/Python3-Training/DatMan/blob/master/FunctionMachines/Adv02.py
# Short:   https://youtube.com/shorts/urRnkGywVEE?si=p5de5R-vNky65rCc
# Video:   https://youtu.be/ZXcPPkn3JIc
# Related: https://www.youtube.com/@TotalPythoneering
# Author: Randall Nagy
# Version: 2.0.b
#endregion

# Key values are automatically assigned, when absent.

import os
import os.path
import shelve

# Something to store:
#region
class Person:
    def __init__(self, name, address, balance):
        self.name = name
        self.address = address
        self.balance = balance

#endregion

class MyShelf:
    # Internals:
    #region
    NEXT_KEY = "next_key"
    def __init__(self, file, object_, sync=False):
        self._file = file
        self._sync = sync
        self._dbm = None
        self._open()
        self._close()
        self._source = {'key':'', 'value':object_}

    def _exists(self):
        ''' See if the dbm file exists 
        True if so, False if no.
        '''
        return os.path.exists(f'{self._file}.dat')

    def _clear(self):
        ''' Empty the database. Always returns None.
        '''
        try:
            if self._open():
                self._dbm.clear()
                self._close()
        except:
            pass

    def _open(self):
        ''' If the dbm file is not 
        there, it will be created. '''
        if self._dbm:
            return True
        try:
            self._dbm = shelve.open(self._file, 'c')
            return True
        except:
            self._dbm = None
        return False

    def _close(self):
        ''' Closes the file, if open.'''
        if not self._dbm:
            return True
        try:
            if self._sync:
                self._dbm.sync()
            self._dbm.close()
            self._dbm = None
            return True
        except:
            self._dbm = None
        return False

    def _get_next_key(self):
        self._open()
        if not MyShelf.NEXT_KEY in self._dbm:
            self._dbm[MyShelf.NEXT_KEY] = 0
        value = int(self._dbm[MyShelf.NEXT_KEY])
        self._dbm[MyShelf.NEXT_KEY] = value + 1
        self._close()
        return str(value)

    def _create(self, value):
        key = self._get_next_key()
        if self._open():
            self._dbm[key] = value
            if self._close():
                return key
        return False

    def _read(self, key):
        result = self.source()
        result['key'] = key
        try:
            if self._open():
                result['value'] = self._dbm[key]
                self._close()
        except Exception as ex:
            print(ex)
        return result

    def _update(self, key, value):
        if self._open():
            self._dbm[key] = value
            if self._close():
                return self._read(key)
        return False

    def _delete(self, key):
        value = None
        if self._open():
            try:
                value = self._dbm.pop(key)
                self._dbm.close()
                return True
            except:
                return False
        return not value is None

    def _param_ok(self, record):
        if not record:
            return False
        if not isinstance(record, dict):
            return False
        for key in self._source:
            if key not in record:
                return False
        return True
    #endregion

    # Public:
    #region
    def count(self):
        self._open()
        count = len(self._dbm)
        if count > 0:
            count -= 1 # ignore next_key row
        self._close()
        return count

    def source(self): # S1
        ''' Get record keys, with data types. '''
        return dict(self._source)

    def sync(self, record): # S2
        ''' Scenario:
        Add a record if none found. Update record, if found.
        Raise verbose exception on error.
        Return record key on success.
        '''
        if not self._param_ok(record):
            raise Exception("Invalid input. Please verify .source.")
        value = record['key']
        if not value:
            key = self._create(record['value'])
            if key:
                return self._read(key)
        else:
            if self._update(record['key'], record['value']):
                return record
        raise Exception("Unable to access database.")

    def search(self, query): # S3
        ''' Scenario:
        Return a record matching query.
        Raise verbose exception on error.
        '''
        if not callable(query):
            return None
        if not self._open():
            raise Exception("Database not found.")
        for key in self._dbm:
            value = self._dbm[key]
            if not isinstance(value, self._source['value']):
                continue
            trool = query(key, value)
            if trool is True:
                record = self.source()
                record['key'] = key
                record['value'] = value
                yield record
                continue
            if trool is False:
                break
            else:
                continue
        self._close()
        return None # Safe coding, is no accident ...

    def delete(self, query): # D1
        ''' Scenario: 
        Remove any record matching query.
        Raise verbose exception on error.
        Returns number of records deleted.
        '''
        if not callable(query):
            return 0
        count = 0
        if not self._open():
            raise Exception("Database not found.")
        for key in dict(self._dbm): # Better!
            value = self._dbm[key]
            if not isinstance(value, self._source['value']):
                continue
            react = query(key, value)
            if react == True:
                value = self._dbm.pop(key)
                if value != None:
                    count += 1
                    yield {'key':key, 'value':value} # (ahem)
                    continue
                else:
                    self._close()
                    raise Exception(
                        f"Unable to remove {record['key']}")
            elif react == False:
                break
        self._close()
        return count

    def deleteTo(self, query, SaveFN): # D2
        ''' Save deleted records to a JSON file.
        Previous contents, if any, will be deleted.
        Return the number of items deleted / saved to same.'''
        import json
        if not callable(query):
            return 0
        count = 0
        with open(SaveFN, 'w') as fh:
            print("[", file=fh)
            for record in self.delete(query):
                    if (count):
                        print(",", file=fh)
                    hit = {
                        'tag':str(record['key']),
                        'value':str(record['value'].__dict__)
                        }
                    json.dump(hit, fh)
                    count += 1
            print("]", file=fh)
        return count
    #endregion

    # Test Cases:
#region
if __name__ == '__main__':
    # TC0000: Clean start
    #region
    TEST_FILE = "~test.shelf"
    test = MyShelf(TEST_FILE, Person)
    if test._exists():
        test._clear()
    #endregion
    # TC1000: Basic object persistence
    #region
    record = test.source()
    obj = record['value']
    record['value'] = obj("Nagy", "foo@bar.net", 123.654)
    record = test.sync(record)
    assert(record)
    #endregion
    # TC1100: Verify object persistence
    #region
    assert(test.count() == 1)
    #endregion
    # TC1200: Multi-record creation
    #region
    record = test.source()
    record['value'] = Person("Zookie", "Wookie@Zookie.star", 12345.626)
    recordU = test.sync(record)
    assert(recordU)
    assert(test.count() == 2)
    #endregion
    # TC1300: Unary update
    #region
    recordU['value'].address = "Bingo"
    record = test.sync(recordU)
    assert(record)
    count = 0
    def bing(a, b):
        if b.address == "Bingo":
            return True
    for record in test.search(bing):
        count += 1
    assert(count == 1)
    assert(test.count() == 2)
    #endregion
    # TC2000: Basic deletion
    #region
    count = 0
    for record in test.delete(bing):
        count += 1
    assert(count == 1)
    assert(test.count() == 1)
    for _ in test.delete(lambda a, b: True):
        pass
    #endregion
    # TC2100: Re-Population
    #region
    data = []
    record = test.source()
    record['value'] = Person("Able", "Able@Able.star", 1000)
    data.append(test.sync(record))
    record = test.source()
    record['value'] = Person("Baker", "Baker@Able.star", 2000)
    data.append(test.sync(record))
    record = test.source()
    record['value'] = Person("Charley", "Charley@Able.star", 3000)
    data.append(test.sync(record))
    record = test.source()
    record['value'] = Person("Delta", "Delta@Able.star", 4000)
    data.append(test.sync(record))
    record = test.source()
    record['value'] = Person("Espsi", "Espsi@Able.star", 5000)
    data.append(test.sync(record))
    assert(test.count() == len(data))

    class Goal:
        def __init__(self, record):
            self.record = record
            self.bDone = False
        def __call__(self, key, value):
            if self.bDone:
                return False
            if key == self.record['key']:
                if value == self.record['value']:
                    self.bDone = True
                    return True

    for record in data:
        row = test.search(Goal(record))
    #endregion
    # TC3000: Basic deletion to-file
    #region
    import json
    BFN = "~backup.tmp"
    assert(test.deleteTo(lambda a, b: True, BFN) == len(data))
    assert(os.path.exists(BFN))
    with open(BFN) as fh:
        guts = json.load(fh)
        assert(len(guts) == len(data))
    os.unlink(BFN)
    #endregion

#endregion

