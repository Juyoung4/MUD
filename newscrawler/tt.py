from datetime import datetime
import csv
now = datetime.now()
now = str(now)
print(now.split())

str1= "2019-11-11"
print(str1.split('-')[0])

str2="2019.11.11. 오후 7:47"
print(str2.split())

print( open('./Article_IT과학_2019-11-11.csv','r',encoding='euc-kr').readline().split(',')[-1])
f=open('./Article_IT과학_2019-11-11.csv','r',encoding='euc-kr').readline().split(',')[-1]
p=f.split()[0].split()[0].split('.')
p = '-'.join([p[i] for i in range(len(p)-1)])
print(type(datetime.strptime(p,'%Y-%m-%d').date()))




