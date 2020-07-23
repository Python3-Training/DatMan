#!/usr/bin/env python3
# Meta:
#region
# License: MIT
# File: Adv05_Shelves.py
# Mission: Use S3D2 over the core 'shelve' Package
# Related:  https://github.com/Python3-Training/DatMan
# Playlist: https://youtu.be/utazxKN7uJA
# Author: Randall Nagy
# Version: 1.0
#endregion

# Note: Conversion from `dbm` to `shelve` was pretty
# much in-place. Because we are perisiting objects, not 
# serializing to octets (bytes,) Python strings
# are queried (i.e. we had to drop the 'b' before
# 'Bingo'.)

import os
import os.path
import shelve

class MyShelf:
    # Internals:
    #region
    def __init__(self, file, sync=False):
        self._file = file
        self._sync = sync
        self._dbm = None
        self._open()
        self._close()
        self._source = {"key":'', "value":object}

    def _exists(self):
        ''' See if the dbm file exists 
        True if so, False if no.
        '''
        return os.path.exists(f'{self._file}.dat')

    def _clear(self):
        ''' Empty th database. Always returns None.
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

    def _create(self, key, value):
        if self._open():
            self._dbm[key] = value
            return self._close()
        return False

    def _read(self, key):
        result = None
        try:
            if self._open():
                result = self._dbm[key]
                self._close()
        except:
            pass
        return result

    def _update(self, key, value):
        return self._create(key, value)

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
        self._close()
        return count

    def source(self): # S1
        ''' Get record keys, with data types. '''
        return self._source

    def sync(self, record): # S2
        ''' Scenario:
        Add a record if none found. Update record, if found.
        Raise verbose exception on error.
        Return record key on success.
        '''
        if not self._param_ok(record):
            raise Exception("Invalid input. Please verify .source.")
        value = self._read(record['key'])
        if not value:
            if self._create(record['key'], record['value']):
                return record
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
        count = 0; zState = 1
        while zState > 0:
            if not self._dbm:
                if not self._open():
                    raise Exception("Database not found.")
            for key in self._dbm:
                value = self._dbm[key]
                react = query(key, value)
                if react == True:
                    value = self._dbm.pop(key)
                    if value != None:
                        count += 1
                        yield {'key':key, 'value':value} # (ahem)
                        self._close()
                        zState = 9
                        break
                    else:
                        zState = 6
                        self._close()
                        raise Exception(
                            f"Unable to remove {record['key']}")
                elif react == False:
                    zState = 8
                    self._close()
                    break
                else:
                    zState = 7
            if zState == 9:
                zState = 1
            else:
                zState = 0
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
                        'value':str(record['value'])
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
    TEST_FILE = "~test.dbm"
    test = MyShelf(TEST_FILE)
    if test._exists():
        test._clear()
    #endregion
    # TC1000: Basic serilaization
    #region
    record = test.source()
    record['key'] = "TestKey"
    record['value'] = "TestValue"
    assert(test.sync(record))
    #endregion
    # TC1100: Verify serialization
    #region
    assert(test.count() == 1)
    #endregion
    # TC1200: Multi-record creation
    #region
    record = test.source()
    record['key'] = "TestKey2"
    record['value'] = "TestValue2"
    assert(test.sync(record))
    assert(test.count() == 2)
    #endregion
    # TC1300: Unary update
    #region
    record['value'] = "Bingo"
    assert(test.sync(record))
    count = 0
    def bing(a, b):
        if b == "Bingo": # 'b' no longer required.
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
    data = [
        {'key':'ab lew', 'value':'this is a test'},
        {'key':'ShaZ\tip', 'value':'this\nisa\ttest'},
        {'key':' pook\nie', 'value':''},
        {'key':'\r\n', 'value':'  '},
        {'key':'bingite', 'value':'wannite'},
        ]
    for record in data:
        test.sync(record)
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

