def main():
    fReader = open('test.json','r')
    lines = []
    for line in fReader:
        if int(line.split(' ')[1])>=15 :
            lines.append(line)

    fReader.close()
    fWriter = open('v_users.txt','w')
    for line in lines:
        fWriter.write(line.split(' ')[0]+'\n')

if __name__=='__main__':
    main()