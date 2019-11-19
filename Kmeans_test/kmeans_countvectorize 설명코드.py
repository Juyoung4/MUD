# CountVectorizer (API Reference)
# : 문서목록에서 각 문서의 feature(문장의 특징) 노출수를 가중치로 설정한 BOW 벡터를 만든다.
import CountVectorizer
vectorize = CountVectorizer(
    tokenizer=tokenizer,
    min_df=2    # 예제로 보기 좋게 1번 정도만 노출되는 단어들은 무시하기로 했다
                # min_df = 0.01 : 문서의 1% 미만으로 나타나는 단어 무시
                # min_df = 10 : 문서에 10개 미만으로 나타나는 단어 무시
                # max_df = 0.80 : 문서의 80% 이상에 나타나는 단어 무시
                # max_df = 10 : 10개 이상의 문서에 나타나는 단어 무시
)

# 문장에서 노출되는 feature(특징이 될만한 단어) 수를 합한 Document Term Matrix(이하 DTM) 을 리턴한다
X = vectorize.fit_transform(rawdata)

print(
    'fit_transform, (sentence {}, feature {})'.format(X.shape[0], X.shape[1])
)
# fit_transform, (sentence 5, feature 7)

print(type(X))
# <class 'scipy.sparse.csr.csr_matrix'>

print(X.toarray())

# [[0, 1, 2, 0, 0, 0, 1],
# [0, 1, 1, 0, 0, 0, 2],
# [1, 0, 0, 2, 1, 1, 0],
# [1, 0, 0, 1, 0, 0, 0],
# [0, 0, 0, 3, 1, 1, 0]]

# 문장에서 뽑아낸 feature 들의 배열
features = vectorize.get_feature_names()