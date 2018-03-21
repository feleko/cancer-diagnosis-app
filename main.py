import os
import csv


def cvs_reader(path):
    reader = csv.reader(open(path), delimiter=' ', quotechar='|')
    return list(reader)


def main():
    path = 'csv/'
    for top, dnames, fnames in os.walk(path):
        for fname in fnames:
            cvs_reader(os.path.join(top, fname))
            

main()
