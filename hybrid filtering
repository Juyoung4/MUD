import requests
import json

import self as self
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import math
import copy
import time


class Recommendation:
    def __init__(self):
        try:
            self.article = requests.get(url="http://34.84.147.192:8000/news/articles/").json()
            self.recommend = requests.get(url="http://34.84.147.192:8000/news/recommend/").json()
            self.rating = requests.get(url="http://34.84.147.192:8000/news/rating/").json()
            self. user_id = requests.get(url="http://34.84.147.192:8000/news/users/").json()
        except Exception as e:
            print(e)

    # pearson 유사도
    def pearson(self, name1, name2):

        sumX = 0
        sumY = 0
        sumPowX = 0
        sumPowY = 0
        sumXY = 0
        count = 0
        data_dic = {}

        for i in self.rating:
            data_dic.update({i['user_id'] : {}})
        
        for i in self.rating:
            for j in data_dic:
                if i['user_id'] == j:
                    data_dic[j].update({i['news_summary'] : i['score']})
 
        for i in data_dic[name1]:
            if i in data_dic[name2]:
                sumX+=data_dic[name1][i]
                sumY+=data_dic[name2][i]
                sumPowX+=pow(data_dic[name1][i],2)
                sumPowY+=pow(data_dic[name2][i],2)
                sumXY+=data_dic[name1][i]*data_dic[name2][i]
                count+=1

        try:
            (sumXY - ((sumX * sumY) / count)) / math.sqrt(
               (sumPowX - (pow(sumX, 2) / count)) * (sumPowY - (pow(sumY, 2) / count)))

        except:
            return -1
        else:
            return (sumXY - ((sumX * sumY) / count)) / math.sqrt(
                (sumPowX - (pow(sumX, 2) / count)) * (sumPowY - (pow(sumY, 2) / count)))

    # 유사도 높은 순 리스트
    def top_match(self, name):

        result_list = []

        user = list(set([i["user_id"] for i in self.rating]))

        for i in user:
            if name != i:
                result_list.append((self.pearson(name, i), i))
        result_list.sort()
        result_list.reverse()
        return result_list

    # 클러스터 id 가져오기
    def getClusterid(self, news_id):

        news_id_list = []
        result = []
        for i in news_id:
            news_id_list.append(i[1])

        for i in self.article:
            if i['news_id'] in news_id_list:
                result.append(i['cluster_id'])

        result = list(set(result))
        return result


    # 협업 필터링
    def getRecommendation(self, person):

        result = self.top_match(person)
        score = 0
        result_list = []
        score_dic = {}
        sim_dic = {}
        data_dic = {}

        for i in self.rating:
            data_dic.update({i['user_id'] : {}})
        
        for i in self.rating:
            for j in data_dic:
                if i['user_id'] == j:
                    data_dic[j].update({i['news_summary'] : i['score']})
        
        
        for sim,name in result:
            if sim <0.5: continue
            for news in data_dic[name]:
                if news not in data_dic[person]:
                    score += sim * data_dic[name][news]
                    score_dic.setdefault(news, 0)
                    score_dic[news] += score
                    sim_dic.setdefault(news, 0)
                    sim_dic[news] += sim
            score = 0

        for key in score_dic:
            score_dic[key] = score_dic[key] / sim_dic[key]
            if score_dic[key] < 4: continue
            result_list.append((score_dic[key], key))

        if not result_list:
            s,n = max(zip(data_dic[person].values(), data_dic[person].keys()))
            cluster_id = self.getContentsbased(n)
        else:
            cluster_id = self.getClusterid(result_list)

        for i in self.recommend:
            if i['user_id'] == person:
                if i['cluster_id'] in cluster_id:
                    cluster_id.remove(i['cluster_id'])
                    if not cluster_id:
                        s,n = max(zip(data_dic[person].values(), data_dic[person].keys()))
                        cluster_id = self.getContentsbased(n)
                


        for cluster in cluster_id:
            data = {"user_id" : person, "cluster_id" : cluster}
            try:
                res = requests.post(url = "http://34.84.147.192:8000/news/recommend/",data =data).json()
            except Exception as e:
                print(e)

    # 콘텐츠 필터링
    def getContentsbased(self, news_id):

        results = {}
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),)
        s = []
        e = []
        index = 0
        for i in self.article[:500]:
            s.append([index, i['summary'], i['news_id']])
            e.append(i['summary'])
            index += 1
        tfidf_matrix = tf.fit_transform(e)
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        for idx, summary, id in s:
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], s[i][2]) for i in similar_indices]
            results[id] = similar_items[:5]
        result = results[news_id][:5]

        cluster_id = self.getClusterid(result)

        return cluster_id

if __name__ == "__main__":
    user_id = requests.get(url="http://34.84.147.192:8000/news/rating/").json()

    Recommender = Recommendation()
    user = list(set([i["user_id"] for i in user_id]))
    sched = BackgroundScheduler()
    

    sched.start()
    for i in user:
        sched.add_job(Recommender.getRecommendation, 'cron', hour='7', minute'30', id=None, args=[i])
        sched.add_job(Recommender.getRecommendation, 'cron', hour='13', minute'30', id=None, args=[i])
        sched.add_job(Recommender.getRecommendation, 'cron', hour='16', minute'30', id=None, args=[i])
        sched.add_job(Recommender.getRecommendation, 'cron', hour='19', minute'30', id=None, args=[i])
        sched.add_job(Recommender.getRecommendation, 'cron', hour='22', minute'30', id=None, args=[i])
        sched.add_job(Recommender.getRecommendation, 'cron', hour='1',, minute'30' id=None, args=[i])

    while True:
        print("wait")
        time.sleep(1)







