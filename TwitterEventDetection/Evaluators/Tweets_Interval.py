'''
Created on 2015年5月14日

@author: Henry Ching
'''
from locale import atoi
import os
import codecs
import re
import sqlite3


class s_data(object):
    """
    get and store serialized data
    """
    def __init__(self):
        """

        :rtype : object
        """
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

def get_burst_terms(burst_term_info):
    interval = 0
    path = '../../serialized/burst_terms'
    with codecs.open(path, encoding='utf-8') as f:
        for line in f:
            li_ne = line.split(' ')
            if li_ne[0]=='Interval':
                new_interval = int(li_ne[1].replace(':',''))
                if(interval > new_interval):
                    new_interval = interval + 1
                if (new_interval-interval)>1:
                    for i in range(interval+1, new_interval):
                        burst_term_info.append([]) #no burst term in that period
                interval = new_interval
                burst_term_info.append([])
            elif li_ne[0] == '\n':
                pass
            else:
                burst_term_info[interval].append(li_ne[0])

if __name__ == '__main__':
    burst_term_info = [[], ] #each item is a time interval, and each interval includes all burst_terms
    get_burst_terms(burst_term_info)
    serialized_data = s_data()

    dbname = 'idcount.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    '''
    c.execute("create table new_id(id varchar(20),total integer)")
    c.execute("INSERT INTO new_id SELECT id,sum(count) as total FROM id GROUP BY id ORDER by total")
    conn.commit()
    '''
        
    datapath = '../../serialized'
    dirlist = os.listdir(datapath)
    output = codecs.open(os.path.join(datapath, "hotspot.txt"), "w", "utf-8")
    output1 = codecs.open(os.path.join(datapath, "mass_eval.txt"), "w", "utf-8")

    count = 0
    for path in dirlist:
        if not (path.startswith('burst') or path.startswith('hot') or path.startswith('mass')):
            interval = atoi(path[0:4])
            maxtoken = 0
            maxid = 0
            token_list = []
            if interval < 163:
                with codecs.open(os.path.join(datapath, path), encoding='utf-8') as f:
                    for line in f:
                        serialized_data.get_serialized_data(line)
                        token_counter = 0
                        tmp_list = []

                        for tokens in serialized_data.tokens:
                            for i_tokens in burst_term_info[interval]:
                                if tokens == i_tokens:
                                    token_counter += 1
                                    tmp_list.append(i_tokens)
                                    break
                        if token_counter > maxtoken:
                            maxtoken = token_counter
                            maxid = serialized_data.fid
                            token_list = tmp_list
                output.write(
                    str(interval) + ':' + str(token_list) + ':' + str(maxid) + "\r\n")

                if maxid:
                    t = (maxid,)
                    c.execute("SELECT total FROM new_id WHERE id=?", t)
                    query = c.fetchall()
                    maxcount = query[0][0]

                    t = (maxcount,)
                    c.execute("SELECT * FROM new_id WHERE total >?", t)
                    len1 = len(c.fetchall())
                    c.execute("SELECT * FROM new_id")
                    len2 = len(c.fetchall())

                    output1.write(
                        str(interval) + ':' + str(len1/len2) + '\r\n')
                else:
                    output1.write(
                        '0:0\r\n'
                    )
        count += 1
        print(str(count) + "finished")
    output.close()
    output1.close()





