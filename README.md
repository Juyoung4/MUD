# MUD
정종설  프로젝트

### news crawler
현재 뉴스 crawler는 네이버 뉴스 포털 사이트를 기반으로 crawling한다.
이때, 얻을 수 있는 카테고리는 '생활과학','IT/과학','경제','사회','정치','세계','오피니언'으로
총 7개이다. 
### news headline create using machine learning
dataset을 구축하고 data 전처리 과정과
train, test 과정을 통해  headline을 추출한다.
 
 - tensorflow를 사용하고 그 버전은 1.18.0이다.
 - CUDA 9.0 버전 사용
 - CUDNN 7.2.5 버전 사용
