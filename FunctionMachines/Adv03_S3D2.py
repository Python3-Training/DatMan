#!/usr/bin/env python3
# License: MIT
# File: Adv03_S3D2.py
# Mission: Implement a Source, Sync, Search, and Delete Pattern.
# Related: https://github.com/Python3-Training/DatMan
#   Video: https://youtu.be/utazxKN7uJA
# Author: Randall Nagy
# Version: 1.1.1
import os
import os.path
import json


class S3D2:
    '''
    Source, Sync, Search, and Delete + Backing Delete 
    records using JSON.
    '''

    def __init__(self, record_dict, home_folder=None, unikey=True):
        ''' Parameters:
        home_folder: Location / folder to store data.
            If home folder does not exist, it will be created. 
            Default home director is the pwd.
        unikey: Case-insensitivity for key lookup. 
            Intended for POSIX Systems, where multi-case FNs ok.
            Caveat MS Windows - still awaiting POSIX promises?
            Default is insensitivity, so all happy. 
        '''
        if isinstance(record_dict, dict):
            self._unikey = unikey
            self._source = record_dict
        else:
            self._source = None
        self.data_dir = os.getcwd().replace("\\", "/")
        if home_folder:
            try:
                if not os.path.exists(home_folder):
                    os.mkdir(home_folder)
                home_folder = home_folder.replace("\\", "/")
                if not home_folder.endswith("/"):
                    home_folder = home_folder + "/"
                self.data_dir = home_folder
            except:
                pass

    def _create_filename(self, key):
        if self._unikey:
            return f"{self.data_dir}{key.lower()}.json"
        else:
            return f"{self.data_dir}{key}.json"

    def _base_name(self, file):
        return file.replace(".json", "")

    def _create(self, record, bOverwrite=False):
        ''' 
        Create + return a matching record.
        Return record created, as re-read.
        False if unable to overwrite, 
        None on error. 
        '''
        if not isinstance(record, dict):
            return None
        try:
            file = self._create_filename(record['Name'])
            if os.path.exists(file) and not bOverwrite:
                return False
            with open(file, "w") as fh:
                json.dump(record, fh)
            return self._read(record['Name'])
        except:
            return None

    def _update(self, record):
        ''' Return a matching record, else None '''
        return self._create(record, True)

    def _exists(self, key):
        ''' See if the record exists 
        True if so, False if no.
        '''
        return os.path.exists(self._create_filename(key))

    def _read(self, key):
        ''' Return a matching record, else None '''
        try:
            file = self._create_filename(key)
            if not os.path.exists(file):
                return None
            with open(file) as fh:
                return json.load(fh)
        except:
            return None

    def _delete(self, key):
        ''' Remove and return the matching record, else None '''
        record = read()
        if record:
            try:
                file = create_filename(key)
                os.unlink(file)
                return record
            except:
                return None

    def _list_files(self):
        for file in os.listdir(self.data_dir):
            if not file.endswith(".json"):
                continue
            yield self.data_dir + file

    def source(self): # S1
        ''' Get record keys, with data types. '''
        return self._source

    def sync(self, record): # S2
        ''' Scenario:
        Add a record if none found. Update record, if found.
        Raise verbose exception on error.
        Return record key on success.
        '''
        record = self._create(record, True)
        if not record:
            raise Exception("Unable to access file system.")
        return record

    def search(self, query): # S3
        ''' Scenario:
        Return a record matching query.
        Raise verbose exception on error.
        '''
        if not callable(query):
            return None
        for file in self._list_files():
            record = None
            with open(file) as fh:
                record = json.load(fh)
            if record:
                trool = query(record)
                if trool is True:
                    yield record
                if trool is False:
                    break
            else:
                raise Exception(f"Error: Unable to read {file}.")
        return None # Safe coding, is no accident ...

    def delete(self, query): # D1
        ''' Scenario: 
        Remove any record matching query.
        Backup deleted data to file, when specified.
        Raise verbose exception on error.
        Returns number of records deleted.
        '''
        if not callable(query):
            return 0
        for file in self._list_files():
            record = None
            with open(file) as fh:
                record = json.load(fh)
            if record:
                trool = query(record)
                if trool is True:
                    os.unlink(file)
                    yield record
                if trool is False:
                    break
            else:
                raise Exception(f"Error: Unable to read {file}.")
        return None # Safe coding, is no accident ...

    def deleteTo(self, query, SaveFN): # D2
        ''' Save deleted records to a JSON file.
        Previous contents, if any, will be deleted.
        Return the number of items deleted / saved to same.'''
        if not callable(query):
            return None
        count = 0
        with open(SaveFN, 'w') as fh:
            print("[", file=fh)
            for hit in self.delete(query):
                try:
                    if (count):
                        print(",", file=fh)
                    json.dump(hit, fh)
                    count += 1
                except ex:
                    raise ex
            print("]", file=fh)
        return count

# Test Cases:
#region
if __name__ == '__main__':

    def filter_name(a):
        if a['Name'] == "Name":
            return True
        return None
#region
# TC1000: Data-location creation
    source = {
            "Name":'', "Address":'', 
            "Phone":'', "Years": 0, 
            "Balance":0.00
        }
    test = S3D2(source, "./testing")
    assert(os.path.exists(test.data_dir))

# TC1100: Data-location creation, AE
    assert(os.path.exists(test.data_dir))
    test = S3D2(source, "./testing")
#endregion
#region
# TC1110: Clean-folder verification
    for foo in test.delete(lambda a: True):
        pass
    count = 0
    for foo in test.delete(lambda a: True):
        count += 1
    assert(count == 0)
#endregion
#region
# TC1200: Bad-data creation
    record = test.source()
    assert(record)
    try:
        test.sync(record)
        assert(False)
    except:
        pass
#endregion
#region
# TC1300: Valid-data creation
    for key in record:
        record[key] = key
    result = test.sync(record)
    for key in result:
        assert(result[key] == record[key])
#endregion
#region
# TC1400: Data update (count verified)
    for key in record:
        if not key == "Name":
            record[key] = key + "2"
    result2 = test.sync(record)
    for key in result2:
        assert(result2[key] == record[key])
    count = 0
    for rec in test.search(filter_name):
        count += 1
    assert(count == 1)
#endregion
#region
# TC1500: Data Clone / New Record
    frec = result2
    frec["Name"] = "New Record"
    result = test.sync(frec)
    for key in frec:
        assert(result[key] == frec[key])
    count = 0
    for record in test.search(lambda a: True):
        count += 1
    assert(count == 3)
#endregion
#region
# TC1600: Delete testing (Type 1 - No backup)
    count = 0
    for foo in test.delete(filter_name):
        count += 1
    assert(count == 1)
    count = 0
    for foo in test.delete(filter_name):
        count += 1
    assert(count == 0)
#endregion
#region
# TC1610: Verify non-callable detection
    count = 0
    for _ in test.search(''):
        count += 1
    assert(count == 0)
    for _ in test.search(''):
        count += 1
    assert(count == 0)
#endregion
#region
# TC1700: Delete testing (Type 2 - Backup -w- verify)
    BFN = "~backup.tmp"
    assert(test.deleteTo(lambda a: True, BFN) == 2)
    assert(os.path.exists(BFN))
    with open(BFN) as fh:
        guts = json.load(fh)
        assert(len(guts) == 2)
        boog = guts[1]
        for key in boog:
            assert(boog[key] == frec[key])
    os.unlink(BFN)
#endregion
#region
# TC1800: Clean-folder verification
    count = 0
    for foo in test.delete(filter_name):
        count += 1
    assert(count == 0)
#endregion

#endregion

