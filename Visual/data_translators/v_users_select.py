import os
import os.path
import xlrd
import sys

#enabled to skip almost empty charts
#only records V users appeared more than once
def main():
    path = r'/Users/Adward/Documents/ZJU/SRTP/TestData/'
    cnt = 0
    v_users = {}

    for parent, dirs, files in os.walk(path):
        for f in files:
            s = os.path.join(parent,f)
            if '.DS_Store'==f:
                continue
            try:
                workbook = xlrd.open_workbook(s)
            except Exception,e:
                print str(e)

            table = workbook.sheets()[2]
            colnames =  table.row_values(0)
            totalRowNum = table.nrows
            for rownum in range(1,totalRowNum):
                id = table.row_values(rownum)[0]
                province = table.row_values(rownum)[2]
                verified = table.row_values(rownum)[10]
                if verified==1 :
                    if v_users.has_key(id):
                        v_users[id][0] += 1
                    else:
                        v_users[id] = [1,province]

    fileWriter = open("v_users.txt",'w')
    for i in range(len(v_users.keys())):
        if v_users[v_users.keys()[i]][0] >= 15:
            fileWriter.write(v_users.keys()[i]+' '+str(int(v_users[v_users.keys()[i]][1]))+'\n')
    fileWriter.close()
    return
if __name__=='__main__':
    main()