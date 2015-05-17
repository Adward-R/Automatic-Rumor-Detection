__author__ = 'Adward'
import os
import sys
import codecs
import sqlite3

def db_init(dbname):
    conn = sqlite3.connect(dbname+'.db')
#    c = conn.cursor()
#    c.execute('CREATE TABLE "%s" (token text, timestamp integer, id integer, rt_id integer)' % dbname)
    conn.commit()
    conn.close()


def db_insert(dbname):
    '''
    Insert serialized data into its corresponding table (by date) in database,
    in form of (token, id), where "id" actually "rt_id";
    much redundancy due to the tremendous cost of DISTINCT operations, yet redundancy might be somewhat useful.
    '''
    #case: seems some duplication among rows, but very few.
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    files = []
    #TODO change path
    path = './serialized/'
    file_lst = os.listdir(path)
    for fn in file_lst:
        files.append(os.path.join(path, fn))
    for fn in files:
        table_name = str(fn).seplit('_')[1] #date
        c.execute('CREATE TABLE if not exists "%s" (token text, id integer)' % table_name)
        conn.commit()
        with codecs.open(fn, encoding='utf-8', errors='ignore') as f:
            try:
                for line in f:
                    li_ne = line.strip('\n').strip('\r').strip('"').strip(']')#.strip('\\')
                    li_ne = li_ne.split(',')
                    #id, timestamp = li_ne[0], li_ne[1].replace(' ','').replace(':','')
                    id = li_ne[0]
                    #TODO retweeted_id = ...
                    for _token in li_ne[2:]:
                        token = _token.strip('"').strip('[').strip(" ").strip("'")
                        c.execute('INSERT INTO "%s" VALUES (?,?)' % table_name, (token, id))
                        conn.commit()
                    #TODO for _rt_id in ... (insert into another table the [original-post->various-reposts] relation)
            except:
                print(line)
    conn.close()

#high cost, deprecated
#def cnt_retweet_id(dbname):
#    conn = sqlite3.connect(dbname+'.db')
#    c = conn.cursor()
#    for token in c.execute('SELECT DISTINCT token FROM "%s"' % dbname):
#        rt_id = c.fetchone('SELECT id FROM "%s" WHERE token=? ORDER BY timestamp ASC' % dbname, token)

def db_print(dbname):
    conn = sqlite3.connect(dbname+'.db')
    c = conn.cursor()
    select_result = c.execute('SELECT * FROM "%s" WHERE token="watch"' % "20150113")
    cnt = 0
    for row in select_result:
        cnt += 1
    print(cnt)
        #break #just for test

if __name__=='__main__':
    dbname = 'token2tweet'

    #uncomment the following functions when it is needed; insertion may take quite a while.

    db_insert(dbname)
    #db_print(dbname)