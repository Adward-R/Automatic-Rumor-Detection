__author__ = 'Adward'
import codecs
import sqlite3

def get_burst_tuples(burst_term_info):
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

    print(burst_term_info)

    for idx in range(0,burst_term_info.__len__()):
        if burst_term_info[idx]!=0:
            token_pool = []
            for token in burst_term_info[idx]:
                token_pool.append(token)
                #inter.remove(token)
            burst_term_info[idx] = []
            leng = token_pool.__len__()
            for i in range(0,leng-1):
                for j in range(i+1,leng):
                    burst_term_info[idx].append((token_pool[i],token_pool[j]))


def tuple2id(id_count, burst_term_info, dbname, start_hour, start_date, end_date):
    rt_count = []
    for i in range(1600):
        rt_count.append(0)
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for inter in range(burst_term_info.__len__()):
        if burst_term_info[inter] != 0:
            for tup in burst_term_info[inter]:
                ids0 = []
                ids1 = []
                for date in range(start_date, end_date+1):
                    #make ids0 and ids1 pre-sorted to apply quick intersecting algorithm
                    ids0 += c.execute('SELECT DISTINCT id FROM "%s" WHERE token=? ORDER BY id ASC ' %str(date), (tup[0],))
                    ids1 += c.execute('SELECT DISTINCT id FROM "%s" WHERE token=? ORDER BY id ASC ' %str(date), (tup[1],))
                #till now, there can be a few duplicates in both ids0 and ids1
                #quick intersection begins
                ids = [] #all ids that correspond to the very token under processing
                p1, p2 = 0, 0
                while p1<ids0.__len__() and p2<ids1.__len__():
                    tmp = ids0[p1][0]
                    if tmp==ids1[p2][0]:
                        if ids.__len__()==0 or ids[-1]!=tmp: #in order to eliminate duplicates
                            ids.append(ids0[p1][0])
                        p1 += 1
                        p2 += 1
                    elif ids0[p1][0]<ids1[p2][0]:
                        p1 += 1
                    else:
                        break
                #quick intersection ends

                for id in ids:
                    count = 0
                    for date in range(start_date, end_date+1):
                        count_result = c.execute('SELECT COUNT(*) FROM "%s" WHERE id=?' %str(date), (id,))
                        for cnt in count_result:
                            count += cnt[0] #cnt is a tuple with only one element
                            break
                    if count>=0: #TODO actually count cannot be used to determine any hotspot in an online algorithm
                        #id_count.append([id, count, start_hour + inter])
                        try:
                            rt_count[count] += 1
                        except:
                            print(str(tup)+' : '+str(id)+' : '+str(count)+' : '+str(start_hour))
                        with open('burst_id_from_tuple', 'a') as f:
                            f.write(str(tup)+' : '+str(id)+' : '+str(count)+' : '+str(start_hour)+'\n')

    conn.close()
    with open('burst_tuple_2_id_line_chart_data.tsv','a') as f:
        f.write('xspan\tyspan\n')
        for i in range(1600):
            f.write(str(i)+'\t'+str(rt_count[i])+'\n')

if __name__=='__main__':
    burst_term_info = [0,] #each item is a time interval, and each interval includes all burst_terms
    id_count = [] #each item is a 3-tuple, including [id, id's count, time when detected as burst]
    dbname = 'token2tweet.db'
    start_hour = 2015011318 #interval 1: 18:00-19:00
    start_date = 20150113
    end_date = 20150115

    get_burst_tuples(burst_term_info)
    print(burst_term_info)
    tuple2id(id_count, burst_term_info, dbname, start_hour, start_date, end_date)
    print(id_count)