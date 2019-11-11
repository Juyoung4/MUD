from datetime import datetime
import datetime
import csv
now = datetime.datetime.now()
str1= "2019-11-11"
print(str1.split('-')[0])

str2="2019.11.11. 오후 7:47"
print(str2.split())

print( open('./Article_IT과학_2019-11-11.csv','r',encoding='euc-kr').readline().split(',')[-1])
f=open('./Article_IT과학_2019-11-11.csv','r',encoding='euc-kr').readline().split(',')[-1]
datee=f.split()[0].split()[0].split('.')
print('-'.join(datee))
datee = '-'.join([datee[i] for i in range(len(datee)-1)]) + " " + f.split()[2]
print("da",datee)
total_date = datee + " " + f.split()[2]
datee = datetime.datetime.strptime(datee, '%Y-%m-%d %I:%M')

if f.split()[1] == '오후':
    datee += datetime.timedelta(hours=12)
print(datee)

# datee=datetime.datetime.strptime(datee,'%Y-%m-%d').date()
# print(datee)

tag = datetime.datetime.strptime('2019-11-11 06:46:00', '%Y-%m-%d %H:%M:%S')
old = datetime.datetime.strptime('2019-11-11 22:17:00', '%Y-%m-%d %H:%M:%S')
if tag > old:
    print("yes")
else: print("no")





