# -*- coding: utf-8 -*-
from __future__ import print_function
from datetime import datetime

# +++++++++++++++++++++++++++++++++++++
# 최종 크롤러!!!
# ++++++++++++++++++++++++++++++++++++
from time import sleep
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
import os
import platform
import calendar
import requests
import re
import datetime
import csv
import json


from lexrankr import LexRank
from apscheduler.schedulers.background import BackgroundScheduler
import time




#excepion
class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return str(self.message)


#article parser
class ArticleParser(object):
    special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]')
    content_pattern = re.compile('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0')

    @classmethod
    def clear_content(cls, text):
        # 기사 본문에서 필요없는 특수문자 및 본문 양식 등을 다 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_content = re.sub(cls.special_symbol, ' ', newline_symbol_removed_text)
        end_phrase_removed_content = re.sub(cls.content_pattern, '', special_symbol_removed_content)
        blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
        content = ''
        for i in range(0, len(blank_removed_content)):
            # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지움
            if reversed_content[i:i + 2] == '.다':
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    @classmethod
    def clear_headline(cls, text):
        # 기사 제목에서 필요없는 특수문자들을 지움
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_headline = re.sub(cls.special_symbol, '', newline_symbol_removed_text)
        return special_symbol_removed_headline

    @classmethod
    def find_news_totalpage(cls, url):
        # 당일 기사 목록 전체를 알아냄
        try:
            totlapage_url = url
            request_content = requests.get(totlapage_url)
            document_content = BeautifulSoup(request_content.content, 'html.parser')
            headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))
            return int(match[0])
        except Exception:
            return 0

#article crawler
class ArticleCrawler(object):
    def __init__(self):

        self.date = {'date': 0, 'time': 0}
        self.user_operating_system = str(platform.system())

    @staticmethod
    def make_news_page_url(category_url, date):
        made_urls = []
        year,month,day=date.split('-')[0],date.split('-')[1],date.split('-')[2]
        url = category_url + year + month + day
        # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
        # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
        totalpage = ArticleParser.find_news_totalpage(url + "&page=10000")
        for page in range(1, totalpage + 1):
            made_urls.append(url + "&page=" + str(page))
        return made_urls

    @staticmethod
    def get_url_data(url, max_tries=10):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def crawling(self, category_name,q):
        global old
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104,
                           'IT_science': 105, 'opinion': 110}

        # Multi Process PID
        count = 0
        print(category_name + " PID: " + str(os.getpid()))

        #date 정의
        now = str(datetime.datetime.now()).split()
        self.date['date'] = now[0]
        self.date['time'] = now[1]

        # 기사 URL 형식(sid1은 category id, date는 date)
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(self.categories.get(category_name)) + "&date="

        # 오늘 기사를 수집합니다[나중에는 시간 단위까지 포함시켜서 crawling]
        day_urls = self.make_news_page_url(url, self.date['date'])
        print(category_name + " Urls are generated")
        print("The crawler starts")
        print(old)

        for URL in day_urls:
            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = self.get_url_data(URL)

            document = BeautifulSoup(request.content, 'html.parser')

            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            post_temp = document.select('.newsflash_body .type06_headline li dl')
            post_temp.extend(document.select('.newsflash_body .type06 li dl'))

            # 각 페이지에 있는 기사들의 url 저장
            post = []
            for line in post_temp:
                post.append(line.a.get('href'))  # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
            del post_temp

            self.new = post[0]
            for content_url in post:  # 기사 URL
                # 크롤링 대기 시간
                if category_name == "economy":
                    if content_url == old[0]:
                        old[0] = self.new
                        return
                if category_name == "IT_science":
                    if content_url == old[1]:
                        old[1] = self.new
                        return
                if category_name == "society":
                    if content_url == old[2]:
                        old[2] = self.new
                        return
                if category_name == "politics":
                    if content_url == old[3]:
                        old[3] = self.new
                        return
                sleep(0.01)

                # 기사 HTML 가져옴
                request_content = self.get_url_data(content_url)
                try:
                    document_content = BeautifulSoup(request_content.content, 'html.parser')
                except:
                    continue

                try:
                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    text_headline = text_headline + ArticleParser.clear_headline(
                        str(tag_headline[0].find_all(text=True)))

                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                    # if not text_sentence:  # 공백일 경우 기사 제외 처리
                    #     continue
                    if len(text_sentence.split('. ')) < 5:
                        continue

                    # 기사 언론사 가져옴
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # 언론사 초기화
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # 공백일 경우 기사 제외 처리
                        continue

                    #뉴스 작성된 시간 가져옴
                    tag_date = document_content.find_all('span', {'class': 't11'})
                    tag_date=re.sub('<.+?>','',(str(tag_date[0]))).strip()
                    text_date = '' #date 초기화
                    text_date = text_date + tag_date
                    tag_date_datetime = text_date.split()[0].split('.')
                    tag_date_datetime = '-'.join(
                        [tag_date_datetime[i] for i in range(len(tag_date_datetime) - 1)]) + " " + text_date.split()[2]
                    tag_date_datetime = datetime.datetime.strptime(tag_date_datetime, '%Y-%m-%d %H:%M')
                    if text_date.split()[1] == '오후':
                        tag_date_datetime += datetime.timedelta(hours=12)
                    if not text_date:
                        continue


                    resultdata = [news_date, category_name, text_company, text_headline, text_sentence, content_url, tag_date_datetime]
                    #print("c",resultdata)
                    q.put(resultdata)
                    count += 1

                    #print("put{}!".format(count))
                    del text_company, text_sentence, text_headline
                    del tag_company
                    del tag_content, tag_headline
                    del request_content, document_content

                except Exception as ex:  # UnicodeEncodeError ..
                    # wcsv.writerow([ex, content_url])
                    del request_content, document_content
                    pass


    def start(self):
        # MultiProcess crawling start(each category)
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,q,))
            proc.start()



count = 0
def smry(q):
    while True:
        try:
            print("smry start")
            global count
            data = q.get()
            count += 1
            #print("get{}!".format(count))
            lexrank = LexRank()
            lexrank.summarize(data[4]) #data[4] (본문)가져와서 요약
            summaries = lexrank.probe(3) #3줄요약, summaries 타입은 list
            data[4] = '. '.join(summaries)+'.' #요약된 내용 다시 .으로 join후 저장
            print(data) #db에 저장되어야 하는 최종 결과
            db_store(data)
            # for summary in summaries:
            #     print(summary)
        except (IndexError,ValueError,AttributeError):
            pass
            # 입력데이터가 이상한 값이어서 요약문이 안나올 때 에러처리 #입력데이터가 None으로 들어올때 에러처리
def db_store(data):
    URL = "http://34.84.147.192:8000/news/articles/"
    data = {
        "headline": data[3],
        "summary": data[4],
        "url": data[5],
        "pub_date": data[6],  # Shuld be in datetime format
        "category": data[1],  # This is news category
        "cluster_id": "1f4f3d79-192a-409c-b824-091ae97bfccd",  # This is Default cluster ID for null value
    }
    try:
        res = requests.post(url=URL,
                            data=data).json()  # This will post data to database and return the colume back and convert to json
        print(res['news_id'])  # This will show the newly created news id
        res = requests.get(url=URL)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    q = Queue()
    ####크롤러####
    Crawler = ArticleCrawler()
    # ####스케줄러로 크롤러 제어####
    sched = BackgroundScheduler()
    sched.start()
    old=[]
    category={"economy":'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=011&aid=0003653323',"IT_science":'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=144&aid=0000642801'
              ,'society':'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=102&oid=023&aid=0003487612','politics':'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=100&oid=214&aid=0000994552'}

    ##경제 :5분/ 사회:3분/ 정치:7분/IT:15분.
    if "economy" in category:
        old.append(category["economy"])
        sched.add_job(Crawler.crawling, 'cron', minute="5", id='test_1',args=["economy", q])  # argssms 배열로 넣어주어야한다.
    if "IT_science" in category:
        old.append(category["IT_science"])
        sched.add_job(Crawler.crawling, 'cron', minute="15", id='test_2', args=["IT_science", q])  # argssms 배열로 넣어주어야한다.
    if "society" in category:
        old.append(category["society"],)
        sched.add_job(Crawler.crawling, 'cron', minute="3", id='test_3', args=["society", q])  # argssms 배열로 넣어주어야한다.
    if "politics" in category:
        old.append(category["politics"])
        sched.add_job(Crawler.crawling, 'cron', minute="7", id='test_4', args=["politics", q])  # argssms 배열로 넣어주어야한다.


    ####요약####
    process_summary = Process(target=smry, args=(q,))
    process_summary.start()

    while True:
        print("running!!")
        time.sleep(1)

    #Crawler.start()
    q.close()
    q.join_thread()