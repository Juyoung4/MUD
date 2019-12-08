from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import pandas as pd

#Dataset불러오기#DB에서 가져오기도 해야함
class call_Dataset:

    def __init__(self):
        import requests
        # articles 테이블에서 크롤링된 데이터를 불러온다.
        rawDatasetjson ={'results':[]}
        try:
            print('DB연결 성공')
            rawDatasetjson = requests.get(url="http://34.84.147.192:8000/news/articles/?limit=21551")
            if rawDatasetjson.status_code == 200:
                rawDatasetjson =rawDatasetjson.json()
                print(rawDatasetjson)
            else:
                print('Bad Request')
        except Exception as e:
            print('DB 연결 실패')
        #url로 불러온 rawDatasetjson은 { ~~:~~~,~~;~~,'results':['news_id:~~,headline:~~....]}이런형태로되있으므로 원하는것 results에
        self.rawDatasetresult = rawDatasetjson['results']
        #크롤링된 데이터를 Dataframe으로 변환 ---->최종 dataframe 형식 Dataset은 변수명'self.df'
        self.originaldf = pd.DataFrame(self.rawDatasetresult)
        self.df = pd.DataFrame(columns=['category','news_id','headline','cluster_id'])
        self.df = self.originaldf[['category','news_id','headline','cluster_id']]

    # 카테고리선택
    def data_in_Category(self,category_Index):
        print('data_in_Category')
        self.category_Index =category_Index  #category는 "economy""IT_science""society""politics"
        self.df = self.df[self.df['category']==self.category_Index]
        print(category_Index,"의 기사개수 : ",len(self.df))
        print(list(self.df['cluster_id']))
        print(set(list(self.df['cluster_id'])))
        print(len(set(list(self.df['cluster_id']))))

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
        first_K, first_index,first_length = self.find_K(self.sK,self.eK,6,200)

        #2차 구간나누기 : 3칸씩 400으로
        if (first_index == first_length): #1차구간중 마지막 구간에 해당한다면
            second_K,second_index,second_length = self.find_K(first_K-5,self.eK,3,300)
        else:
            second_K,second_index,second_length = self.find_K(first_K-5,first_K+5,3,300)

        #3차 구간나누기 :
        thrid_K =self.find_K(second_K,second_K+3,1,600)[0]
        print('final_optimal_K',thrid_K)
        return thrid_K

#근접기사 찾기 : return은 거리순으로 cluster 내 뉴스를 정렬했을 때, 40개 초과시 해당되는 뉴스들의 index값으로
class closed_news:
    def __init__(self,kmeansmodel,l,d):
        print('closed_news')
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
        default_cluster=[]
        for i in range (len(self.label)):
            dis_list_in_cluster = self.dis_list[base:base+self.label.count(i)]
            dis_list_in_cluster.sort(key=lambda x: x[2])
            base += self.label.count(i)
            # cluster_id 당 기사 개수가 40개가 크면 (default값으로 부여해줌)
            if(self.label.count(i)>40):
                for m in range(40 , self.label.count(i)):
                    #거리 정렬순으로 했을때 해당 cluster_id 속 40번째가 초과되는 뉴스기사들의 index를 default_cluster 리스테 넣어주기
                    default_cluster.append(dis_list_in_cluster[m][0])
        return (default_cluster)

#DB에 Clusterid 부여하기
class store_Clusterid:
    def __init__(self,finalData,rawDataresult):
        print('store_clusterid Class')
        self.url_articles ="http://34.84.147.192:8000/news/articles/"
        self.url_clsuter = "http://34.84.147.192:8000/news/clusters/"
        self.finalData = finalData
        self.rawDataresult = rawDataresult

    #새로 정의 된 label (Cluster Table에서 고유 UUID값 받아온 cluster_id list =====>lable)
    def creatCluster(self,clusterHeadline, clusterSummary):
        import requests
        postUrl = self.url_clsuter
        if clusterHeadline:
            data = {
                "cluster_headline": clusterHeadline,
                "cluster_summary": clusterSummary
            }
            res = requests.post(url=postUrl, data=data)
            if res.status_code == 201:
                data = res.json()
                return data['cluster_id']
            else:
                print('Bad Request')
                return None
        else:
            print('Cluster Headline Must not be null!')
            return None
    def replace_clusterid_to_uuid(self):
        print('replace_clusterId_to_uuid')
        label = self.finalData['cluster_id']
        labelset = list(set(label))
        del(labelset[labelset.index('07f269a8-3ae6-4994-abfd-e2cb2d4633f3')])
        # New Cluster Headline and Summary
        newClusterHeadline = 'This is cluster Headline'
        newClusterSummary = 'This is cluster Summary'

        cluster_uuid_list =[]
        #생성된 Cluster 갯수만큼 headline,summary 값 보내주기
        for i in range (len(labelset)):
            cluster_uuid_list.append(self.creatCluster(newClusterHeadline,newClusterSummary))

        for i in (labelset):
            # label.replace(i,cluster_uuid_list[i],label.count(i))
            label = list(map(lambda x: cluster_uuid_list[int(i)] if x == i else x, label))
            self.finalData['cluster_id']=label
            # self.rawDataresult['cluster_id']=list(map(str,label))
        return label
    #새로정의된 label을 원래데이터 rawDataresult에 붙어서
    def updateClusterId(self, newClusterIdlist):
        import requests
        # self.rawDataresult=list(self.rawDataresult)
        if  newClusterIdlist:
            print('updateClusterid')
            print(newClusterIdlist)
            # for article in self.rawDataresult.loc[self.rawDataresult['cluster_id']==newClusterId]:
            print(len(self.rawDataresult))
            print(len(newClusterIdlist))
            for i in range( len(self.rawDataresult)):
                article = self.rawDataresult.iloc[i]
                if(newClusterIdlist[i]!='07f269a8-3ae6-4994-abfd-e2cb2d4633f3'):
                    print('if문돌아가는중')
                    try:
                        print('try')
                        article['cluster_id'] = newClusterIdlist[i]
                        res = requests.put(url=self.url_articles + article['news_id'] + '/', data=article.to_dict())
                        if res.status_code == 200:
                            data = res.json()
                            print('Cluster ID Upadated for News : ' + data['news_id'])
                        else:
                            print('Bad Request!')
                    except  :
                        print('Something went wrong when updating the News ID')
                # Tell the user their URL was bad and try a different one

        else:
            print('Cluster ID and News List must not be null')
    def store(self):
        a=self.replace_clusterid_to_uuid()
        print('store')
        self.updateClusterId(a)

#한번에 K_mean 모두 실행 class
class run_kmeans:
    def __init__(self,category_index,start_Kn,end_Kn):
        # 카테고리 선택해서 data 들고오기
        get_rawData = call_Dataset()
        # caall_Dataset Class에서 self.df는 ['category','news_id','headline','cluster_id']Dataframe
        self.category = category_index
        self.rawData = get_rawData.data_in_Category(category_index)  # DB에서 들고오는 일단은 제목에 해당되는 rawData
        self.DBjson=get_rawData.df
        self.rawDataresult = get_rawData.originaldf[get_rawData.originaldf['category']==category_index] #해당카테고리의 모든 데이터가 있는 dataframe
        print()
        self.sK = start_Kn
        self.eK = end_Kn

    def play(self):
        p =preprocessing(self.rawData)
        preprocessed_Data =p.result()
        o =optimal_K(preprocessed_Data,self.sK,self.eK)
        k = o.final_find_K() #최적의 K
        finalkmeans =KMeans(n_clusters=k, init= 'k-means++',n_init=600).fit(preprocessed_Data)

        label =finalkmeans.labels_
        distance = finalkmeans.transform(preprocessed_Data)
        c=closed_news(finalkmeans,label,distance)
        default_index = c.default_index_news() #default를 줘야하는 뉴스기사 index들 리스트

        label2 = list(map(str, label))
        for i in default_index:
            label2[i]="07f269a8-3ae6-4994-abfd-e2cb2d4633f3"

        # 최종은 label2
        Final_Data = pd.DataFrame(columns=['news_id', 'cluster_id'])
        Final_Data['news_id'] = self.DBjson['news_id']
        Final_Data['cluster_id'] = label2

        s = store_Clusterid(Final_Data,self.rawDataresult)
        s.store()
        print("Clustering ALL Success")


    #고정 K 주었을때
    def play_fixK(self):
        p = preprocessing(self.rawData)
        preprocessed_Data = p.result()
        # o = optimal_K(preprocessed_Data, self.sK, self.eK)
        # k = o.final_find_K()  # 최적의 K
        finalkmeans = KMeans(n_clusters=20, init='k-means++', n_init=100).fit(preprocessed_Data)


        label =finalkmeans.labels_
        distance = finalkmeans.transform(preprocessed_Data)
        c=closed_news(finalkmeans,label,distance)
        default_index = c.default_index_news() #default를 줘야하는 뉴스기사 index들 리스트

        label2 = list(map(str, label))
        for i in default_index:
            label2[i]="07f269a8-3ae6-4994-abfd-e2cb2d4633f3"

        # 최종은 label2
        Final_Data = pd.DataFrame(columns=['news_id', 'cluster_id'])
        Final_Data['news_id'] = self.DBjson['news_id']
        Final_Data['cluster_id'] = label2

        s = store_Clusterid(Final_Data,self.rawDataresult)
        s.store()
        print(self.category," : Clustering ALL Success")
