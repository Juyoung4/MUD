from sklearn.cluster import KMeans

import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
# %matplotlib inline 주피터노트북에서 그래프 표현하기위한 라인
#파이참에서는 그래프 하단에 plt.show()할것

#데이터프레임을 형성해서 1~100가지의 숫자로 50개의 x,y데이터 생성
df = pd.DataFrame(columns = ['x','y'])
import random
for i in range(50):
    df.loc[i] = [random.randrange(1,100),random.randrange(1,100)]

#산점도 그래프
sb.lmplot('x','y', data = df, fit_reg = False, scatter_kws = {"s":50})
#fit_reg = False는 회귀 옵션 제거, scatter_kws = {"s":50}는 산점도 그래프 점 크기 설정
plt.title('K-means Example')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

#그 다음 생성도니 데이터프레임을 객체로 변환해주고 클러스트 갯수를 정해 분류한다.
#할떄마다 바뀐다.
df_obj = df.values #numpy를 사용하기 위해 객체로 변환
kmeans = KMeans(n_clusters = 3).fit(df_obj) #3개의 클러스트 발생
print(kmeans.cluster_centers_)
print(kmeans.labels_)

#다음은 생성된 라벨을 새로운 컬럼값으로 저장하고 산점도 그래프를 그려준다.
df['cluster'] = kmeans.labels_

sb.lmplot('x','y', data = df, fit_reg = False, scatter_kws = {"s":150}, hue = "cluster")
plt.title('K-means Example')
plt.show()