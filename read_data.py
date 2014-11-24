
import  xdrlib ,sys
import xlrd
def open_excel(file= 'file.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
def excel_table_byindex(file= 'file.xlsx',colnameindex=0,by_index=2):
    fileHandle = open('train.txt','w')
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    colnames =  table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
        fileHandle.write('<1>')
        row = table.row_values(rownum)
        if row:
             #app = {}
            for i in (6,7,8,9,11,):
            #for i in range(1,len(colnames)+1):
                #app[colnames[i]] = row[i-1]
                fileHandle.write(' <')
                fileHandle.write(str(i))
                fileHandle.write('>:<')
                fileHandle.write(str(row[i-1]))
                fileHandle.write('>')
             #list.append(app)
            fileHandle.write('\n')
    return 0
    #return list

def excel_table_byname(file= 'file.xlsx',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows
    colnames =  table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def main():
   tables = excel_table_byindex()
   #for row in tables:
   #    print row

#   tables = excel_table_byname()
#   for row in tables:
#       print row

if __name__=="__main__":
    main()