# !/usr/bin/python
# -*- coding: gbk -*-
import sys
import getopt
from ase.io import read
from ase.visualize import view

def printUsage():
    print('''usage: test.py -i <input> -o <output>
    test.py --in=<input> ''')


def view_model():
    file_dir = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["in="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(-1)
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
        elif opt in ("-i", "--in"):
            file_dir = arg

    try:
        atoms = read(file_dir)
        view(atoms)
    except:
        raise RuntimeError

if __name__ == "__main__":
    view_model()

