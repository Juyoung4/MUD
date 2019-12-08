# -*- coding: utf-8 -*-
import csv
import os
from lexrankr import LexRank
lexrank=LexRank()
os.chdir("./")
file_unity=open('jp3.csv','a',encoding='CP949', newline="")
wcsv = csv.writer(file_unity)


file1 = open('mergefile.csv','r',encoding='CP949')
line = csv.reader(file1)

count = 0

for i in line:
    count += 1
    if 35182 < count:
        if not (len(i[1].split('. '))<5):
            lexrank.summarize(i[1])
            summ = lexrank.probe(3)
            wcsv.writerow([i[0],'. '.join(summ)+'.'])
        else:
            wcsv.writerow([i[0],i[1]])
    

