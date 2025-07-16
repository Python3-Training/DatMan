#!/usr/bin/env python3
# License: MIT
# File: Adv01.py
# Mission: Demonstrate a simple way to manage data, via 
# a plausable C.R.U.D signature.
# Source:  https://github.com/Python3-Training/DatMan/blob/master/FunctionMachines/Adv01.py
# Short:   https://youtube.com/shorts/urRnkGywVEE?si=p5de5R-vNky65rCc
# Related: https://www.youtube.com/@TotalPythoneering
# Author: Randall Nagy
# Version: 1.0.d

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
