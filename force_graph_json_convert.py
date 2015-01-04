import os
import os.path
import xlrd
import sys

#enabled to skip almost empty charts
#only records V users appeared more than once
def main():
    path = r'/Users/Adward/Documents/ZJU/SRTP/TestData/'

    v = []
    province = []
    pReader = open('v_users.txt','r')
    nodeNum = 0
    for line in pReader:
        v.append(line.split(' ')[0])
        province.append([line.split(' ')[0],line.split(' ')[1].strip('\n')])
        nodeNum += 1
    pReader.close()
    link = []
    for i in range(nodeNum):
        tmp = []
        for j in range(nodeNum):
            tmp.append(0);
        link.append(tmp)

    
    #fileWriter = open("weibo1.json",'w')
    #fileWriter.write('{\n "name": "weibo",\n "children": [')
    for parent, dirs, files in os.walk(path):
        for f in files:
            s = os.path.join(parent,f)
            if '.DS_Store'==f:
                continue
            try:
                workbook = xlrd.open_workbook(s)
            except Exception,e:
                print str(e)
            nodes = []
            table = workbook.sheets()[2]
            totalRowNum = table.nrows
            for rownum in range(1,totalRowNum):
                id = table.row_values(rownum)[0]
                if id in v:
                    nodes.append(v.index(id))
            for i in range(len(nodes)):
                for j in range(i+1,len(nodes)):
                    link[nodes[i]][nodes[j]] += 1

            
                

    f = open("_users.json",'w')
    f.write('{\n "nodes": [')
    cnt = 0
    for man in province:
        if cnt!=0 :
            f.write(',')
        f.write('\n  {"name": '+man[0]+', "group": '+man[1]+'}')
        cnt += 1
    f.write('\n ],\n "links": [')
    cnt = 0
    for i in range(nodeNum):
        for j in range(i+1,nodeNum):
            if link[i][j]>0 :
                if cnt!=0:
                    f.write(',')
                f.write('\n  {"source": '+str(i)+',"target": '+str(j)+',"value": '+str(link[i][j])+'}')
                cnt += 1
    f.write('\n ]\n}')
    f.close()
    
if __name__=='__main__':
    main()