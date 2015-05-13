__author__ = 'Adward'
import codecs
import sqlite3

def get_burst_terms(burst_term_info):
    interval = 0
    path = '../TestData/serialized/burst_terms'
    with codecs.open(path, encoding='utf-8') as f:
        for line in f:
            li_ne = line.split(' ')
            if li_ne[0]=='Interval':
                new_interval = int(li_ne[1].replace(':',''))
                if (new_interval-interval)>1:
                    for i in range(interval+1, new_interval):
                        burst_term_info.append(0) #no burst term in that period
                interval = new_interval
                burst_term_info.append([])
            elif li_ne[0]=='\n':
                pass
            else:
                burst_term_info[interval].append(li_ne[0])

def token2id(id_count, burst_term_info, dbname, start_hour, start_date, end_date):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for inter in range(burst_term_info.__len__()):
        if burst_term_info[inter] != 0:
            for itm in burst_term_info[inter]:
                ids = [] #all ids that correspond to the very token under processing
                for date in range(start_date, end_date+1):
                    ids += c.execute('SELECT DISTINCT id FROM "%s" WHERE token=?' %str(date), (itm,))
                for id in ids:
                    count = 0
                    for date in range(start_date, end_date+1):
                        count += c.execute('SELECT COUNT(*) FROM "%s" WHERE id=?' %str(date), (id,))
                    id_count.append([id, count, start_hour + inter - 1])
    conn.close()

if __name__=='__main__':
    burst_term_info = [0,] #each item is a time interval, and each interval includes all burst_terms
    id_count = [] #each item is a 3-tuple, including [id, id's count, time when detected as burst]
    dbname = 'token2tweet.db'
    start_hour = 2015011318 #interval 1: 18:00-19:00
    start_date = 20150113
    end_date = 20150115

    get_burst_terms(burst_term_info)
    token2id(id_count, burst_term_info, dbname, start_hour, start_date, end_date)
    print(id_count)