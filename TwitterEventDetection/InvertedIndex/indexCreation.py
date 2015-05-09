__author__ = 'Adward'
import os
import sys
import codecs
import sqlite3

def db_init(dbname):
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    c.execute('CREATE TABLE "%s" (token text, timestamp integer, id integer, rt_id integer)' % dbname)
    conn.commit()
    conn.close()

def db_insert(dbname):
    #case: seems some duplication among rows, but very few.
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    files = []
    path = './serialized/'
    file_lst = os.listdir(path)
    for fn in file_lst:
        files.append(os.path.join(path, fn))
    for fn in files:
        with codecs.open(fn, encoding='utf-8') as f:
            for line in f:
                li_ne = line.strip('\n').strip('\r').strip('"').strip(']')#.strip('\\')
                li_ne = li_ne.split(',')
                id, timestamp = li_ne[0], li_ne[1].replace(' ','').replace(':','')
                #TODO retweeted_id = ...
                for _token in li_ne[2:]:
                    token = _token.strip('"').strip('[').strip(" ").strip("'")
                    c.execute('INSERT INTO "%s" VALUES (?,?,?,?)' % dbname, (token, timestamp, id, 0))
                    conn.commit()
                #TODO for _rt_id in ... (insert into another table the [original-post->various-reposts] relation)
    conn.close()

#high cost, deprecated
def cnt_retweet_id(dbname):
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    for token in c.execute('SELECT DISTINCT token FROM "%s"' % dbname):
        rt_id = c.fetchone('SELECT id FROM "%s" WHERE token=? ORDER BY timestamp ASC' % dbname, token)

def db_print(dbname):
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    select_result = c.execute('SELECT * FROM "%s" WHERE token="watch"' % dbname)
    for row in select_result:
        print(row)
        #break #just for test

if __name__=='__main__':
    dbname = 'token2tweet'
    #uncomment the following functions when it is needed; insertion may take quite a while.

    #db_init(dbname)
    #db_insert(dbname)
    db_print(dbname)