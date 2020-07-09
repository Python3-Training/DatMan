#!/usr/bin/env python3
# License: MIT
# File: Adv01.py
# Mission: Demonstrate a simple way to manage data, via 
# a plausable C.R.U.D signature.
# Related: https://www.youtube.com/watch?v=IX9vYXT2NW8
# Author: Randall Nagy
# Version: 1.0

def create():
    print("Create something...")

def read():
    print("Read something...")

def update():
    print("Update something...")

def delete():
    print("Delete something...")

def search():
    print("Search something...")

if __name__ == '__main__':
    options = {
        'c':create, 'r':read, 'u':update, 'd':delete,
        's':search, 'q':quit
        }
    while True:
        op = input("Option: ")
        if op in options:
            options[op]()
        else:
            print("Invalid option. Try again?")
