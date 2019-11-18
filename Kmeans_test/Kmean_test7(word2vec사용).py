##한글 뉴스 기사 데이터 가져오기
import kmeans
import pandas as pd
df = pd.read_csv('./data/news.csv')

#categor ==1은 교육관련기사
df = df[df['category']==1]

#1.자연어처리
from konlpy.tag import Mecab
def tokenize_sentense(text):
    mecab=Mecab()
    return mecab.morphs(text)

tokenized_data =tokenize_sentense(df)
#2.Word2Vec
from gensim.models import Word2Vec as w2v
model = w2v(tokenized_data, size=100, window=2, min_count=50, iter=20, sg=1)
    # 포스태깅된 컨텐츠를 100차원의 벡터로 바꿔라.
    # 주변 단어(window)는 앞뒤로 두개까지 보되, 코퍼스 내 출현 빈도가 50번 미만인 단어는 분석에서 제외해라.
    # CPU는 쿼드코어를 쓰고 100번 반복 학습해라. 분석방법론은 CBOW와 Skip-Gram 중 후자를 선택해라.
# tokenized_data는 2D list로 저장된 값입니다.
# 위의 함수(tokenized_sentence)의 output을 넣어주면 됩니다.

#벡터화
# data : [ ['이', '건', '하나', '의', '글', '입니다',], ['이', '건', '다른', '글', '이죠'], ... ]
# model : data의 각각 하나의 token('이','건','하나','다른' 등)이 word2vec으로 학습된 모델
#K means에서는 하나의 표본당 하나의 벡터값으로 표현되어야한다.
def get_n_tokens(data, model):
    result = []
    word_list = ['택시', '분실', '나눔', '판매', '설문', '공지', '상품', '질문', '연락', '구해요']
    for i,j in enumerate(data):
        dist = [0] * len(word_list)
        if not data[i]:   # 내용이 없는 글
            pass
        elif len(data[i]) == 1:     # 한 토큰으로 된 글
            for l,m in enumerate(word_list):
                try:
                    dist[l] = model.similarity(m, data[0])
                except:
                    continue
        else:     # 한 토큰 이상으로 된 글
            for idx, k in enumerate(j):
                if idx >= 50:   # 토큰 50개만 사용한다.
                    break
                for l,m in enumerate(word_list):
                    try:
                        dist[l] += model.similarity(m, k)
                    except:
                        continue
        result.append([ x/(idx+1) for x in dist])
    return result

#4.K Means
import sklearn.cluster import KMeans as km
inertia = []    # cluster 응집도
for k in range(1,11):    # 10개까지
	model = km(n_cluster = k)
    model.fit(data)
    inertia.append(model.inertia_)
print(inertia)