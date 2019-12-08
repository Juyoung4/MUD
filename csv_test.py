# -*- coding: utf-8 -*-
"""
import csv
import os
import pandas as pd
from lexrankr import LexRank

os.chdir("./")

df = pd.read_csv('merge4.csv',names=[1,2,3,4,5,6])
df = df[:200000]
print(len(df))
df.drop_duplicates()
print(len(df))
print(df[4].head())
print(df[5].head())

df.to_csv('jp.csv',columns=[4,5])
"""
# -*- coding: utf-8 -*-
from lexrankr import LexRank
import csv
file_unity=open('politics.csv','r',encoding='CP949')
line1 = csv.reader(file_unity)

file_unity2=open('society.csv','r',encoding='CP949')
line2 = csv.reader(file_unity2)


file1 = open('jp.csv','w',encoding='CP949', newline="")
wcsv = csv.writer(file1)

count = 0
for k in line1:
    if count == 0: pass
    count += 1

    if len(k[4].split(".")) <= 5:pass
    if count == 100000: 
        break
    else: 
        wcsv.writerow([k[3],k[4]])
#file1.close()
count = 0
file2 = open('jp2.csv','w',encoding='CP949', newline="")
wcsv2 = csv.writer(file2)
for j in line2:
    if count == 0: pass
    count += 1

    if len(j[4].split(".")) <= 5:pass
    if count == 150000: 
        break
    else: 
        wcsv2.writerow([j[3],j[4]])
        
    
