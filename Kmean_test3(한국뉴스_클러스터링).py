#한글뉴스기사 Dataset
#pandas로 import 해서 한글 기사들을 가져오겠습니다.
import pandas as pd
df = pd.read_csv('./data/news.csv')
#이 중 category==1 인 뉴스기사만 추출해 보도록 하겠습니다.category==1인 뉴스기사는 ‘교육’과 관련된 기사입니다.
df = df[df['category']==1]
print(df.head(10))

#preprocessing ( 특수문자 제거 )
import re
def preprocessing(sentence):
    sentence =re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z]', ' ', sentence)
    return sentence
df['content_cleaned'] = df['content'].apply(preprocessing)
content = df['content_cleaned']
print(df.loc[df['category']==1,['content'],])


#sklearn 라이브러리 활용
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

# 군집화 할 그룹의 갯수 정의
n_clusters = 2

#문장 특징추출 준비
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
np.random.seed(0)
from konlpy.tag import Okt
twitter = Okt()
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# tokenizer : 문장에서 색인어 추출을 위해 명사,동사,알파벳,숫자 정도의 단어만 뽑아서 normalization, stemming 처리하도록 함
def tokenizer(raw, pos=["Noun","Alpha","Verb","Number"], stopword=[]):
    return [
        word for word, tag in twitter.pos(
            raw,
            norm=True,   # normalize 그랰ㅋㅋ -> 그래ㅋㅋ
            stem=True    # stemming 바뀌나->바뀌다
            )
            if len(word) > 1 and tag in pos and word not in stopword
        ]

# CountVectrizer로 토큰화
vectorizer = CountVectorizer(tokenizer= tokenizer, min_df = 1)
X = vectorizer.fit_transform(content)
print('fit_transform, (sentence {}, feature {})'.format(X.shape[0], X.shape[1]))
print(vectorizer.get_feature_names())
print(pd.DataFrame(X.toarray()))
# l2 정규화
print('정규화')
X = normalize(X)
print(X)
print('normalize_fit_transform, (sentence {}, feature {})'.format(X.shape[0], X.shape[1]))
print(pd.DataFrame(X.toarray()))


#최적의 K찾기
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
def BestK(X):
    distortions = []
    K = range(1,30)
    for k in K:
        kmeanModel = KMeans(n_clusters=k, init='k-means++',random_state=0)
        kmeanModel.fit(X)
        distortions.append(kmeanModel.inertia_)
        print('for k')
        # distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
    # Plot the elbow
    print('hello')
    plt.plot(K,distortions,marker = 'o')
    plt.xlabel('cluster개수')
    plt.ylabel('SSE')
    plt.show()
    # plt.plot(K, distortions, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel('Distortion')
    # plt.title('The Elbow Method showing the optimal k')
    # plt.show()
BestK(X)

print('그래프그리기')
#산점도 그래프 그리기
import seaborn as sb
def drawgraph(data):
    #fit_reg = False는 회귀 옵션 제거, scatter_kws = {"s":50}는 산점도 그래프 점 크기 설정
    # df = pd.DataFrame( columns= ['x','y'])
    # for i in data:
    #     df.loc[i] =i
    df = pd.DataFrame(X.toarray())
    print(df)
    # df = pd.DataFrame(data.toarray(), columns=vectorizer.get_feature_names())
    ax = df.plot(kind = 'scatter', x = 'X',y='Y',alpha = 0.1, s=300)
    ax.set_xlabel("X layer")
    ax.set_ylabel("Y layer")
    ax.show()
    # sb.lmplot('x','y', data = df, fit_reg = False, scatter_kws = {"s":50})
    # plt.title('K-means Example')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()
# drawgraph(X)

# k-means 알고리즘 적용
# # kmeans = KMeans(n_clusters=100).fit(X)
#
# # trained labels and cluster centers
# centers = kmeans.cluster_centers_
# # labels에 merge
# df['labels'] =  kmeans.labels_

# #간단히 코드 몇 줄 만으로 뉴스기사에대한 clustering이 완료되었습니다.
#
# print()
# print(df.loc[df['labels']==9,['content_cleaned', 'labels','id']])
# print()
# print(df.loc[df['labels']==1,['content_cleaned','labels','id']])
# print()
# for i in (df.loc[df['labels']==9,['id']]):
#     print(df.loc[df['id']==i])
# print()

from IPython.display import display
# describe(df.loc[df['id']==10])
# print(type(df))
# print(df.loc[df['labels']==1])

