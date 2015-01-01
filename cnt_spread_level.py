import os
import os.path
import xlrd
#import xlrlib
import sys
import xlwt

def main():
    path = r'/Users/Adward/Documents/ZJU/SRTP/TestData/'
    for parent, dirs, files in os.walk(path):
        for f in files:
            level = []
            s = os.path.join(parent,f)
            if '.DS_Store'==f:
                continue
            try:
                workbook = xlrd.open_workbook(s)
            except Exception,e:
                print str(e)
            table = workbook.sheets()[0]
            colnames =  table.row_values(0)
            row = []
            totalRowNum = table.nrows
            for rownum in range(1,totalRowNum):
                row.append(table.row_values(rownum))
            for rownum in range(totalRowNum-1):
                #print rownum
                cnt = 0
                ptr = rownum
                while row[ptr][4]!='0': #is not the origin post
                    #print row[ptr][4]
                    cnt += 1
                    for prownum in range(totalRowNum-1):
                        if (row[prownum][0]==row[ptr][4]):
                            ptr = prownum
                            break
                #table.put_cell(rownum+1,8,2,cnt,0) #row,col,ctype,value,xf=0
                level.append(cnt)

            newWorkbook = xlwt.Workbook()
            sheet = newWorkbook.add_sheet('tweet')
            for i in range(totalRowNum):
                for j in range(5):
                    sheet.write(i,j,label=table.cell(i,j).value)
                if (i>0):
                    sheet.write(i,5,label=level[i-1])
                else:
                    sheet.write(0,5,label='spread level')

            newWorkbook.save('/Users/Adward/Documents/ZJU/SRTP/LevelData/'+str(f))
                
if __name__=='__main__':
    main()