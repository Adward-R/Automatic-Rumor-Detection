'''
Created on 2015年5月14日

@author: Henry Ching
'''
import os
import sqlite3
import codecs
import re

class s_data(object):
    """
    get and store serialized data
    """
    def __init__(self):
        self.fid = ''
        self.tokens = []
        self.timestamp = ''

    def get_serialized_data(self, line):

        comma_idx = line.find(',')
        self.fid = line[0:comma_idx]
        line = line[comma_idx + 1:]

        comma_idx = line.find(',')
        self.timestamp = line[0:comma_idx]
        line = line[comma_idx + 1:]

        line = re.sub(r'\[|\]|\'|\"|\r|\n', '', line)
        line = line.replace(' ', '')
        self.tokens = line.split(',')

    def print_data(self):
        print(self.fid)
        print(self.timestamp)
        print(self.tokens)


if __name__ == '__main__':
    serialized_data = s_data()

    datapath = '../../serialized'
    dirlist = os.listdir(datapath)

    dbname = 'idcount.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("create table id(id varchar(20),count integer)")

    counter = 0
    for path in dirlist:
        if not (path.startswith('burst') or path.startswith('hot')):
            with codecs.open(os.path.join(datapath, path), encoding='utf-8') as f:
                for line in f:
                    serialized_data.get_serialized_data(line)
                    t = (serialized_data.fid,)
                    c.execute("insert into id values(?,1)", t)
                    counter += 1
    conn.commit()

    print(counter)
    conn.close()






