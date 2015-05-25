finname = 'mass_eval.txt'
foutname1 = 'mass_eval.tsv'
foutname2 = 'mass_sequel.tsv'
benchmark = [10, 1.0, 0.1, 0.01, 0.001, 0.0001, 0.0001]
interval = 6*[0]
total = 0
with open(finname) as fin:
    for line in fin:
        li_ne = line.split(':')
        if int(li_ne[0])>0:
            total += 1
            ratio = float(li_ne[1]) * 100.0
            for inter in range(6):
                if ratio>benchmark[inter+1] and ratio<benchmark[inter]:
                    interval[inter] += 1
                    break

with open (foutname1, 'w') as fout:
    fout.write('ratio\tcnt\n')
    for i in range(6):
        fout.write(str(i+1)+'\t'+str(interval[i]/total * 100.0)+'\n')

########
with open(foutname2, 'w') as fout:
	fout.write('ratio\tcnt\n')

with open(finname) as fin:
    counter = 0
    for line in fin:
        with open(foutname2, 'a') as fout:
            ratio = float(line.split(':')[1]) * 100
            for i in range(6):
                if ratio>benchmark[i+1] and ratio<benchmark[i]:
                    ratio = i
                    break
            fout.write(str(counter)+'\t'+str(ratio)+'\n')
        counter += 1

