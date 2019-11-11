from konlpy.tag import Mecab
import csv
import os
import re

#stopword
stopwords = ['가운데', '대체로', '간의', '크게', '같', '아니', '있', '되', '두', '받', '많', '크', '좋', '따르', '만들', '시키', '그러', '하나','모르', '데', '자신', '어떤', '명', '앞', '번', '보이', '나', '어떻', '월', '들', '이렇', '점', '싶', '좀', '잘', '통하', '놓','란', '이나', '것', '이', '그', '수', '등', '의', '때', '경우', '및', '를', '대한', '사용', '위', '때문', '약', '제', '후','다른', '중', '이상', '일', '은', '위해', '가지', '시', '로', '세', '과', '다음', '두', '더', '또한', '함', '하나', '우리', '개','관', '속', '가장', '모두', '점', '곳', '전', '또', '통해', '여러', '대해', '안', '즉', '모든', '내', '뒤', '보고', '이후', '데','로서', '다시', '관련', '알', '비', '그것', '나', '일반', '각', '뜻', '정도', '사이', '사실', '도', '따라서', '고', '못', '예', '간', '동안', '매우', '정', '지금', '증', '임', '공', '해', '음', '앞', '번', '볼', '여기', '거나', '자', '부', '인', '날','바로', '대부분', '기', '바', '주로', '뿐', '직접', '부터', '계속', '일부', '주', '재', '아래', '더욱', '초', '각각', '동시', '권','년', '곧', '온', '거의', '먼저', '비롯', '역시', '몇', '반드시', '거', '보', '단', '듯', '가장', '서로', '모든', '에 대한 ',' 수 ', '모두', '의', '에', '대해', '그런데', '으로', '이것', '대로', '것', '그대로', '그리고', '것도', '수가', '이 ', '해야', '지금','할 수가', '할 수', '각종', '요게', '여기', '혹시', '우리', '한번', '이번', '당신', '이렇게', '차고', '어떻게', '뭐', '깜짝', '거지','싶어서', '그래서', '정말', '이런', '도저히', '거죠', '하면은', '이제', '그렇게', '그럼', '많이', '이거', '그거', '저거', '누가', '그래', '그냥', '바로', '누가', '다시', '그래도', '간단히', '거야', '이따', '00', '근데', '결국', '이때', '누가', '그런', '딱', '일단', '보면','하나', '어디', '부터', '원', '위하', '나오', '중', '못하', '그렇', '오', '대하', '한', '지', '하']

#csv file save
os.chdir("./")
doc_ko=open('merge12.csv','w',encoding='utf_8_sig', newline="")
wcsv = csv.writer(doc_ko)

#mecab tokenize
m = Mecab()

file1 = open('merge10.csv','r',encoding='utf_8_sig')
line = csv.reader(file1)

title,content,title1,content1,title2,content2=[],[],[],[],[],[]
m_title,m_content=[],[]
count=1
temp=''
for i in line:
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    i[0] = hangul.sub('',i[0])
    i[1] = hangul.sub('',i[1])
    m_title.append(m.morphs(i[0]))
    m_content.append(m.morphs(i[1]))
    #stop word delete
    for w in m_title:
        if w not in stopwords:
            title.append(w)
    for p in m_content:
        if p not in stopwords:
            content.append(p)

    title1 = ' '.join(title[0])
    title2.append(title1)
    content1 = ' '.join(content[0])
    content2.append(content1)

    
    if count == 100:
        break
    else: 
        count += 1
    title1=''
    title,title1=[],[]
    m_title=[] 
    content1=''
    content,content1,=[],[]
    m_count=[]
    #title1,content1='',''
    #title,content,title1,content1,title2,cotent2=[],[],[],[],[],[]
    #m_title,m_content=[],[] 

for i in range(len(title2)):
     wcsv.writerow([title2[i],content[i]])
