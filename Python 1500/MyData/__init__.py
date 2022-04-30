#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    sys.path.insert(0,'../')

import MyData.MyJSON
import MyData.MyPickle

__all__ = [
    "MyJSON.create", "MyJSON.read",
    "MyJSON.update", "MyJSON.search",
    "MyJSON.list_files", "MyJSON.delete",
    "MyPickle.create", "MyPickle.read",
    "MyPickle.update", "MyPickle.search",
    "MyPickle.list_files", "MyJSON.delete"
           ]
