#한글뉴스기사 Dataset
#pandas로 import 해서 한글 기사들을 가져오겠습니다.
import pandas as pd
df = pd.read_csv('./data/news.csv')
#이 중 category==1 인 뉴스기사만 추출해 보도록 하겠습니다.category==1인 뉴스기사는 ‘교육’과 관련된 기사입니다.
df = df[df['category']==1]
print(df.head(10))

#preprocessing (특수문자 제거)
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

# CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(content)
# l2 정규화
X = normalize(X)

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

# BestK(X)

# k-means 알고리즘 적용
kmeans = KMeans(n_clusters=10).fit(X)

# trained labels and cluster centers
centers = kmeans.cluster_centers_
# labels에 merge
df['labels'] =  kmeans.labels_

#간단히 코드 몇 줄 만으로 뉴스기사에대한 clustering이 완료되었습니다.

print()
print(df.loc[df['labels']==9,['content_cleaned', 'labels','id']])
print()
print(df.loc[df['labels']==1,['content_cleaned','labels','id']])
print()
for i in (df.loc[df['labels']==9,['id']]):
    print(df.loc[df['id']==i])
print()

from IPython.display import display
describe(df.loc[df['id']==10])
# print(type(df))
# print(df.loc[df['labels']==1])

