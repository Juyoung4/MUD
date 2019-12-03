from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import pandas as pd

#Dataset불러오기#DB에서 가져오기도 해야함
class call_Dataset:

    def __init__(self):
        import json
        import requests
        rawDatasetjson ={}
        # articles 테이블에서 크롤릴된 데이터를 불러온다.
        try:
            rawDatasetjson = requests.get(url="34.84.147.192:8000/news/articles/?format=json").json
        except Exception as e:
            print('DB 연결 실패')

        # rawDatadict = json.loads(rawDatasetjson)
        self.df = pd.read_json(rawDatasetjson)
    # 카테고리선택
    def data_in_Category(self,category_Index):
        self.category_Index =category_Index  #category는 "economy""IT_science""society""politics"

        # df = pd.read_csv('./data/news_parkju.csv')  # DB에서 불러오는 걸로 바꿔야함
        # df = df[df['category']==self.category_Index]
        # df_headline = df['headline'].tolist() #제목을 불러올땐 'headline' 이렇게, 내용을불러올땐 'summary'
        self.df = self.df[self.df['category']==self.category_Index]
        df_headline = self.df['headline'].tolist()

        return df_headline

#전처리과정 > 2차원배열 X
class preprocessing:
    #초기화?
    def __init__(self,rawData):
        self.data = rawData
        print('preprocessing init')

    #토큰화함수
    def tokenizer(self,raw,pos=["Noun"], stopword ='[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z]'):
        import pandas as pd
        pd.options.mode.chained_assignment = None
        import numpy as np
        np.random.seed(0)
        from konlpy.tag import Okt
        twitter = Okt()
        return [
            word for word, tag in twitter.pos(
                raw,
                norm=True,  # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
                stem=True  # stemming 바뀌나->바뀌다
            )
            if len(word) > 1 and tag in pos and word not in stopword
        ]

    def result(self):#rawDatas는 call_Dataset Class의 data_in_Category 함수로 사용
        from sklearn.feature_extraction.text import CountVectorizer
        #CountVectorizer로 벡터화, 이때 토큰화는 Class 내 tokenizer 사용
        vectorizer = CountVectorizer(tokenizer = self.tokenizer)
        X=vectorizer.fit_transform(self.data)
        #벡터 정규화처리
        X=normalize(X)
        # X=X.toarray() : distoration구할때 !
        return X

    def draw_result_graph(self):
        #산포도 그래프 그리기 data에 대해
        print('i')

#최적의 K 찾기 > 결과는 K값
class optimal_K:
    def __init__(self,preprocessed_data,start_Kn,end_Kn):
        self.X = preprocessed_data
        self.sK = start_Kn
        self.eK = end_Kn
        print('optimal_K init')

    #Elbow 기법으로 K값에 따른 SSE 그래프 그리기
    def draw_K_graph(self,step,n_init):
        import matplotlib.pyplot as plt
        # import numpy as np
        # from scipy.spatial.distance import cdist
        # distortions = []
        inertias = []
        K = range(self.sK, self.eK,step)
        for k in K:
            kmeanModel = KMeans(n_clusters=k, init='k-means++',n_init=n_init).fit(self.X)
            inertias.append(kmeanModel.inertia_)
            # distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)**2))
        print(inertias)
        #Plot the elbow
        plt.plot(range(self.sK, self.eK,2), inertias, label='Inertia',marker = 'x')
        # plt.plot(range(start_Kn, end_Kn), distortions, label='Distance',marker ='o')
        plt.xlabel('cluster개수')
        plt.ylabel('SSE')
        plt.legend()
        plt.show()

    #Elbow 기법으로 K값에 따른 SSE 튜플형식으로 리스트
    def find_Kdic(self,set_sK,set_eK,step_arg,n_init):
        print('find_Kdic')
        inertias =[]
        K = range(set_sK, set_eK,step_arg)
        for k in K:
            kmeans = KMeans(n_clusters=k, init='k-means++',n_init=n_init)#n_init가 클수록정확해야짐
            kmeans.fit(self.X)
            inertias.append(kmeans.inertia_)
        list_Kdic =dict(zip(K,inertias))
        print(list_Kdic)
        return list_Kdic

    # 기울기가 급격히 완만해지는 구간을 찾는 함수
    def find_K(self,set_sK,set_eK,step_arg,n_init):
        list_Kdic=self.find_Kdic(set_sK,set_eK,step_arg,n_init)
        print('find_K')
        # print(list_Kdic)

        #SSE 기울기
        base = list(list_Kdic.values())[0]
        difference_list =[] #list 속 요소는 list[3]인것은 3과4사이/ sK+2부터 sK+3사이차이 --->차가 처음으로 크다면 즉 sK+3이 적절K
        for i in list_Kdic.values():
            difference_list.append(base-i)
            base =i

        #SSE 기울기 차
        dd_list =[]
        dd_base=difference_list[1]
        for i in difference_list[1:]:
            dd_list.append(dd_base-i)
            dd_base =i

        #최종 optimal K
        length = len(dd_list)
        index = dd_list.index(max(dd_list))
        finalK = (index*step_arg)+set_sK
        print('K = ',finalK)
        return finalK , index, length

    #2단계 구간 나누기 --> 단기간 최적의 K c찾는함수
    def final_find_K(self):
        #1차 구간나누기 : 6칸씩 300으로
        first_K, first_index,first_length = self.find_K(self.sK,self.eK,6,300)

        #2차 구간나누기 : 3칸씩 400으로
        if (first_index == first_length): #1차구간중 마지막 구간에 해당한다면
            second_K,second_index,second_length = self.find_K(first_K-5,self.eK,3,400)
        else:
            second_K,second_index,second_length = self.find_K(first_K-5,first_K+5,3,400)

        #3차 구간나누기 :
        thrid_K =self.find_K(second_K,second_K+3,1,600)[0]
        print('final_optimal_K',thrid_K)
        return thrid_K

#근접기사 찾기
class closed_news:
    def __init__(self,kmeansmodel,l,d):
        print('closed_news')
        print('hi')
        self.model = kmeansmodel
        self.label = l.tolist()
        self.distance = d
        self.dis_list = []
        self.K = max(l)+1

    def default_index_news(self):
        print('choose')
        #dis_list = [ [뉴스 index, cluster_index, 해당클리서터 중심과의 거리],,,,,] 다차원배열
        for i in range (len(self.distance)):
            cluster_index =self.label[i]
            self.dis_list.append([i,cluster_index,self.distance[i][cluster_index]])
        #다차원배열dmf cluster index정렬로
        self.dis_list.sort(key=lambda x:x[1])

        #뉴스index의 clusterindex 배열 label도 cluster index정렬로
        self.label.sort()
        base = 0
        defluat_cluster=[]
        for i in range (len(self.label)):
            print(base)
            print(i)
            dis_list_in_cluster = self.dis_list[base:base+self.label.count(i)]
            dis_list_in_cluster.sort(key=lambda x: x[2])
            base += self.label.count(i)
            if(self.label.count(i)>40):
                print('a')
                print(i)
                print('b',dis_list_in_cluster)
                for m in range(40 , self.label.count(i)):
                    print(m)
                    defluat_cluster.append(dis_list_in_cluster[m][0])
                    print(defluat_cluster)
        print(self.dis_list)
        print(defluat_cluster)
        return (defluat_cluster)

#label_uuid로 바꿔주는 함수
    def make_uuid(self):
        import uuid
        for i in range(len(self.label)):
            self.label[i] = self.label[i].replace(i, uuid.uuid1())
        return self.label,list(set(self.label))

#DB에 Clusterid 부여하기
class store_Clusterid:
    def __init__(self,finalData):

        print('store_clusterid')
        self.url_articles ="34.84.147.192:8000/news/articles/"#"34.84.147.192:8000/news/articles/?format=json"
        self.url_clsuter = "http://34.84.147.192:8000/news/clusters/"
        self.finalData = finalData

    def store(self):
        import requests

        print('d')
        try:
            res = requests.post(url=self.url_clsuter,data=self.finalData).json()
            res = requests.post(url=self.url_articles,data="f").json()
            print()
        except Exception as e:
            print('DB접근 오류')

#한번에 K_mean 모두 실행 class
class run_kmeans:
    def __init__(self,category_index,start_Kn,end_Kn):
        # 카테고리 선택해서 data 들고오기
        get_rawData = call_Dataset()
        self.DBjson=get_rawData.df
        self.rawData = get_rawData.data_in_Category(category_index)  # DB에서 들고오는 일단은 제목에 해당되는 rawData
        self.sK = start_Kn
        self.eK = end_Kn

    def play(self):
        p =preprocessing(self.rawData)
        preprocessed_Data =p.result()
        o =optimal_K(preprocessed_Data,self.sK,self.eK)
        k = o.final_find_K()
        finalkmeans =KMeans(n_clusters=k, init= 'k-means++',n_init=600).fit(preprocessed_Data)

        label =finalkmeans.labels_
        distance = finalkmeans.transform(preprocessed_Data)
        c=closed_news(finalkmeans,label,distance)

        default_index = c.default_index_news()
        label,labelset = c.make_uuid()
        for i in default_index:
            label[default_index[i]]="1f4f3d79-192a-409c-b824-091ae97bfccd"
        #최종은 label
        Final_Data1 =pd.DataFrame(columns=['news_id','cluster_id'])
        Final_Data1.loc[0] =self.DBjson['news_id']
        Final_Data1.loc[1] =label

        Final_Data2 =pd.DataFrame(columns=['cluster_id'])
        Final_Data2.loc[0] = labelset


    def play_fixK(self):
        p = preprocessing(self.rawData)
        preprocessed_Data = p.result()
        # o = optimal_K(preprocessed_Data, self.sK, self.eK)
        finalkmeans = KMeans(n_clusters=25, init='k-means++', n_init=600).fit(preprocessed_Data)

        label =finalkmeans.labels_
        distance = finalkmeans.transform(preprocessed_Data)
        c=closed_news(finalkmeans,label,distance)

        default_index = c.default_index_news()
        label,labelset = c.make_uuid()
        for i in default_index:
            label[default_index[i]]="1f4f3d79-192a-409c-b824-091ae97bfccd"
        #최종은 label
        Final_Data1 =pd.DataFrame(columns=['news_id','cluster_id'])
        Final_Data1.loc[0] =self.DBjson['news_id']
        Final_Data1.loc[1] =label

        Final_Data2 =pd.DataFrame(columns=['cluster_id'])
        Final_Data2.loc[0] = labelset
