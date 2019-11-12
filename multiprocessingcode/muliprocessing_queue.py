# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import os

from lexrankr import LexRank

# +++++++++++++++++++++++++++++++++++++
# 최종 크롤러!!!
# ++++++++++++++++++++++++++++++++++++
from time import sleep
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
import os
import platform
import calendar
import requests
import re
from datetime import datetime
import csv

#excepion
class InvalidCategory(Exception):
    def __init__(self, category):
        self.category = category
        self.message = " is not valid."

    def __str__(self):
        return str(self.category + self.message)
#excepion
class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return str(self.message)

#csv write(here csv delete)
class Writer(object):
    def __init__(self, category_name, date):
        self.user_operating_system = str(platform.system())

        self.category_name = category_name

        self.date = date
        self.date1 = self.date['date']
        self.time1 = self.date['time']

        self.file = None
        self.initialize_file()

        self.wcsv = csv.writer(self.file)

    def initialize_file(self):
        #window와 linux csv 저장 encoding 형식 다름
        if self.user_operating_system == "Windows":
            self.file = open('Article_' + self.category_name + '_' + self.date1+ '.csv', 'w', encoding='euc-kr',newline='')
        # Other OS uses utf-8
        else:
            self.file = open('Article_' + self.category_name + '_' + self.date1+ '.csv', 'w',encoding='utf-8', newline='')

    def get_writer_csv(self):
        return self.wcsv

    def close(self):
        self.file.close()

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
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104,
                           'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.date = {'date': 0, 'time': 0}
        self.user_operating_system = str(platform.system())

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

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
        # Multi Process PID
        count = 0
        print(category_name + " PID: " + str(os.getpid()))

        #date 정의
        now = str(datetime.now()).split()
        self.date['date'] = now[0]
        self.date['time'] = now[1]

        writer = Writer(category_name=category_name, date=self.date)

        # 기사 URL 형식(sid1은 category id, date는 date)
        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(self.categories.get(category_name)) + "&date="

        # 오늘 기사를 수집합니다[나중에는 시간 단위까지 포함시켜서 crawling]
        day_urls = self.make_news_page_url(url, self.date['date'])
        print(category_name + " Urls are generated")
        print("The crawler starts")

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

            for content_url in post:  # 기사 URL
                # 크롤링 대기 시간
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
                    if not text_date:
                        continue

                    # write csv ( here change csv -> database access)
                    #wcsv = writer.get_writer_csv()
                    #wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url, text_date])
                    resultdata = [news_date, category_name, text_company, text_headline, text_sentence, content_url, text_date]
                    print(resultdata)
                    q.put(resultdata)
                    count += 1
                    print("put{}!".format(count))
                    del text_company, text_sentence, text_headline
                    del tag_company
                    del tag_content, tag_headline
                    del request_content, document_content

                except Exception as ex:  # UnicodeEncodeError ..
                    # wcsv.writerow([ex, content_url])
                    del request_content, document_content
                    pass
        writer.close()

    def start(self):
        # MultiProcess crawling start(each category)
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,q,))
            proc.start()





# 각 크롤링 결과 저장하기 위한 리스트 선언
furl_list = []
title_text = []
link_text = []
L_category_text = []
S_category_text = []
date_text = []
contents_text = []
result = {}

now = datetime.now()  # 파일이름 현 시간으로 저장하기

#대주제 -> 소주제 들어가는 함수
def first_crawler():
    url = f'https://terms.naver.com/list.nhn?cid=41703&categoryId=41703'
    bbreq = requests.get(url)
    bbhtml = bbreq.text
    bbsoup = BeautifulSoup(bbhtml, 'html.parser')

    for furls in bbsoup.select('#content > div.subject_wrap > div > ul > li > a'):
        furls = "http://terms.naver.com" + furls["href"]
        furl_list.append(furls)

    return furl_list


#본문가져오기
def get_text(n_url):
    text_detail = []

    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    textlist = bsoup.select('#size_ct > p')

    for txt in textlist:
        # text_detail.append(txt.text)
        return txt.text

#소주제에서 페이지 넘기면서 본문 크롤링
def crawler2(q):
    count = 0
    for url in first_crawler():             # first_crawler()함수로 소주제 링크 목록 가져오기
        for i in range(2,3):                # 페이지 수 100개 - 150000개

            urlp = url + '&page={}'.format(i)
            response = requests.get(urlp)
            html = response.text

            # 뷰티풀소프의 인자값 지정
            #"이 문자열은  html 구조에 맞게 작성되어있음. html 관점에서 이해하라는 것
            soup = BeautifulSoup(html, 'html.parser')

            # 본문전체내용
            for urls in soup.select('div.subject > strong > a:nth-child(1)'):
                urls = "http://terms.naver.com" + urls["href"]
                data = get_text(urls)
                q.put(data)
                count += 1
                print("put{}!".format(count))

count = 0
def smry(q):
    while True:
        try:
            print("smry start")
            global count
            data = q.get()
            count += 1
            print("get{}!".format(count))
            lexrank = LexRank()
            lexrank.summarize(data[4])
            summaries = lexrank.probe(3)
            for summary in summaries:
                print(summary)
        except (IndexError,ValueError,AttributeError):
            pass
            # 입력데이터가 이상한 값이어서 요약문이 안나올 때 에러처리 #입력데이터가 None으로 들어올때 에러처리

    def start(self):
        # MultiProcess crawling start(each category)
        for category_name in self.selected_categories:
            proc = Process(target=self.crawling, args=(category_name,q,))
            proc.start()


if __name__ == "__main__":
    q = Queue()
    #q2 = Queue()

    Crawler = ArticleCrawler()
    Crawler2 = ArticleCrawler()
    Crawler.set_category("IT과학")
    Crawler2.set_category("경제")


    #process_one = Process(target=crawler2, args=(q,))
    process_two = Process(target=smry, args=(q,))
    #process_three = Process(target=smry, args=(q2,))
    Crawler.start()

    Crawler2.start()

    process_two.start()
    #process_three.start()

    #process_one.start()



    q.close()
    q.join_thread()

    ##q2.close()
    #q2.join_thread()
