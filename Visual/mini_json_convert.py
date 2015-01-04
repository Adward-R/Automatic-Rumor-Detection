import os
import os.path
import xlrd
import sys

#enabled to skip almost empty charts
def main():
    path = r'/Users/Adward/Documents/ZJU/SRTP/LevelData/'
    cnt = 0
    for parent, dirs, files in os.walk(path):
        for f in files:
            s = os.path.join(parent,f)
            if '.DS_Store'==f:
                continue
            try:
                workbook = xlrd.open_workbook(s)
            except Exception,e:
                print str(e)
            table = workbook.sheets()[0]
            colnames =  table.row_values(0)
            fre = []
            level = []
            totalRowNum = table.nrows
            for rownum in range(1,totalRowNum):
                fre.append(table.row_values(rownum)[1].split(' '))
                lev = table.row_values(rownum)[5]
                if (int(lev)==0 or int(lev)==1):
                    level.append(0)
                elif (int(lev)==2):
                    level.append(1)
                else:
                    level.append(2)

            _fre = []
            for itm in fre:
                _fre.append([int(itm[0]),int(itm[1])])

            lp = 0 #smallest value
            hp = 0 #biggest value
            for i in range(len(_fre)):
                if _fre[i][0]<_fre[lp][0] or (_fre[i][0]==_fre[lp][0] and _fre[i][1]<_fre[lp][1]):
                    lp = i
                if _fre[i][0]>_fre[hp][0] or (_fre[i][0]==_fre[hp][0] and _fre[i][1]>_fre[hp][1]):
                    hp = i

            #print str(_fre[hp][0])+' '+str(_fre[hp][1])
            #print str(_fre[lp][0])+' '+str(_fre[lp][1])
            duration = (_fre[hp][0]-_fre[lp][0])*24 + (_fre[hp][1]-_fre[lp][1])
            if duration==0:
                continue

            freq = []
            for i in range(24):
                tmp = [0,0,0]
                freq.append(tmp)
            #normalization
            tick = 0
            for itm in _fre:
                itm = ((itm[0]-_fre[lp][0])*24 + (itm[1]-_fre[lp][1]))*1.0/duration*24
                if itm - 24==0.0:
                    itm -= 0.1
                freq[int(itm)][level[tick]] += 1
                tick += 1

            fileWriter = open("./json/"+str(cnt)+".json",'w')
            fileWriter.write('{\n "name": "flare",\n "children": [')
            for i in range(len(freq)):
                if i!=0:
                    fileWriter.write(',')
                fileWriter.write('\n  {"total": '+str(freq[i][0]+freq[i][1]+freq[i][2])+', "level0": '+str(freq[i][0])+', "level1": '+str(freq[i][1])+', "level2": '+str(freq[i][2])+'}')
            fileWriter.write('\n ]\n}')
            fileWriter.close()
            print 'Processing file '+str(f)+' finished.'
            cnt += 1
                
if __name__=='__main__':
    main()