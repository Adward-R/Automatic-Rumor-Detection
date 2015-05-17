import os
import os.path
import xlrd
import sys

#enabled to skip almost empty charts
#only records V users appeared more than once
def main():
    path = r'/Users/Adward/Documents/ZJU/SRTP/TestData/'
    cnt = 0
    repost_users = []

    for parent, dirs, files in os.walk(path):
        for f in files:
            s = os.path.join(parent,f)
            if '.DS_Store'==f:
                continue
            try:
                workbook = xlrd.open_workbook(s)
            except Exception,e:
                print str(e)

            slices = [0,0,0,0]
            table = workbook.sheets()[2]
            totalRowNum = table.nrows
            for rownum in range(1,totalRowNum):
                gender = table.row_values(rownum)[4]
                verified = table.row_values(rownum)[10]
                if gender=='m':
                    if verified==1:
                        slices[0] += 1#repost_users["Verified-Male"] += 1
                    else:
                        slices[2] += 1#repost_users["Unverified-Male"] += 1
                else:
                    if verified==1:
                        slices[1] += 1#repost_users["Verified-Female"] += 1
                    else:
                        slices[3] += 1#repost_users["Unverified-Female"] += 1
            repost_users.append(slices)
            print "Processed "+str(f)
            cnt += 1
            if cnt==400:
                break

    fileWriter = open("../data/donut.json",'w')
    fileWriter.write(str(repost_users).replace("'",'"'))
    fileWriter.close()
    return

if __name__=='__main__':
    main()