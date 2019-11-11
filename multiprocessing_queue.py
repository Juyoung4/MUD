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
def crawler(q):
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
            global count
            data = q.get()
            count += 1
            print("get{}!".format(count))
            lexrank = LexRank()
            lexrank.summarize(data)
            summaries = lexrank.probe(1)
            for summary in summaries:
                print(summary)
        except (ValueError,AttributeError):
            pass
            # 입력데이터가 이상한 값이어서 요약문이 안나올 때 에러처리 #입력데이터가 None으로 들어올때 에러처리

if __name__ == '__main__':
    q = Queue()
    process_one = Process(target=crawler, args=(q,))
    process_two = Process(target=smry, args=(q,))
    process_one.start()
    process_two.start()

    q.close()
    q.join_thread()

    process_one.join()
    process_two.join()

