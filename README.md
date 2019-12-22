# DeepLearning을 이용한 뉴스 요약 서비스
# NEWSSUM MOBILE APPLICATION

[![GitHub issues](https://img.shields.io/github/issues/Juyoung4/MUD)](https://github.com/Juyoung4/MUD/issues) [![GitHub forks](https://img.shields.io/github/forks/Juyoung4/MUD)](https://github.com/Juyoung4/MUD/network) [![GitHub stars](https://img.shields.io/github/stars/Juyoung4/MUD)](https://github.com/Juyoung4/MUD/stargazers) [![GitHub license](https://img.shields.io/github/license/Juyoung4/MUD)](https://github.com/Juyoung4/MUD/blob/master/LICENSE)

본 문서는 묶음 뉴스 요약 본 제공 서비스인 Newsum Application시스템의 요구사항정의서에 대한 상세 설계를 기술한 것이다. 시스템의 인터페이스와 서비스 측면에서 Deep Learning을 이용한 헤드라인 생성 서비스, Lexrank 알고리즘을 이용한 컨텐츠 생성 서비스 개인화 맞춤 뉴스 추천 서비스 등에 대한 상세 설계 방법을 기술하고 있다.

    -	K-means 클러스터링을 이용하여 실시간 뉴스 군집화
    -	Lexrank 알고리즘(추출적 요약)과 Attention mechanism RNN 모델(추상적 요약)을 이용한 본문 요약과 헤드라인 추출
    -	content-based filtering과 collaborated user-based filtering 을 사용하여 사용자에게 뉴스 추천

# 소프트웨어

  - NEWSUM APP - Google Flutter 이용한 Android/iOS APP은 User가 service를 제공받기 위한 User Interface이다 
  - APPLICATION SERVER - Linux Server는 Django rest framework를 통해 User Interface, Newsum server와 HTTP 통신하여 DB에 대해 CRUD 할 수 있다

### NewsSum uses a number of Aplications to work properly:

* [Flutter](https://github.com/flutter/flutter/blob/master/README.md) - Mobile Application
* [Django](https://www.djangoproject.com/) - Backend Server
    - [Django REST framework](https://www.django-rest-framework.org/) - News API

And of course NewsSum itself is open source with a [public repository](https://github.com/Juyoung4/MUD)
 on GitHub.

License
----

[MIT](https://github.com/Juyoung4/MUD/blob/master/LICENSE)
