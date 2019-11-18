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

# CountVectrizer로 토큰화
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(content)
# l2 정규화
X = normalize(X)


#데이터 스케일링
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
scaler.fit_transform(X[0])
feature = scaler.fit_transform(X[0])

#최적의 K찾기
import matplotlib.pyplot as plt

##1.elbow기법
def elbow(X):
    sse = []

    for i in range(1,11):
        km = KMeans(n_clusters=i,algorithm='auto', random_state=42)
        km.fit(X)
        sse.append(km.inertia_)
    plt.plot(range(1,11), sse, marker='o')
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.show()
#elbow(feature)
##2.실루엣기법
import numpy as np
from sklearn.metrics import silhouette_samples
from sklearn.datasets import make_blobs
from matplotlib import cm

def plotSilhouette(X, y_km):
    cluster_labels = np.unique(y_km)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = silhouette_samples(X, y_km, metric = 'euclidean')
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []

    for i, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[y_km == c]
        c_silhouette_vals.sort()
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(i/n_clusters)

        plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0,
                edgecolor='none', color=color)
        yticks.append((y_ax_lower + y_ax_upper)/2)
        y_ax_lower += len(c_silhouette_vals)

    silhoutte_avg = np.mean(silhouette_vals)
    plt.axvline(silhoutte_avg, color = 'red', linestyle='--')
    plt.yticks(yticks, cluster_labels+1)
    plt.ylabel('K')
    plt.xlabel('실루엣 계수')
    plt.show()
#plotSilhouette(feature, y_km)
#실행

k= 4
#
# X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5,
#                   shuffle=True, random_state=0)
# km = KMeans(n_clusters=k, algorithm='auto', random_state=42)
# y_km = km.fit_predict(feature)
# plotSilhouette(feature, y_km)