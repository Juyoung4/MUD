class Article {
  String newsId;
  String headline;
  String summary;
  String url;
  String pubDate;
  String sumDate;
  String category;
  String clusterId;

  Article(
      {this.newsId,
      this.headline,
      this.summary,
      this.url,
      this.pubDate,
      this.sumDate,
      this.category,
      this.clusterId});

  Article.fromJson(Map<String, dynamic> json) {
    newsId = json['news_id'];
    headline = json['headline'];
    summary = json['summary'];
    url = json['url'];
    pubDate = json['pub_date'];
    sumDate = json['sum_date'];
    category = json['category'];
    clusterId = json['cluster_id'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['news_id'] = this.newsId;
    data['headline'] = this.headline;
    data['summary'] = this.summary;
    data['url'] = this.url;
    data['pub_date'] = this.pubDate;
    data['sum_date'] = this.sumDate;
    data['category'] = this.category;
    data['cluster_id'] = this.clusterId;
    return data;
  }
}

class Clusters {
  String clusterId;
  String clusterHeadline;
  String clusterSummary;

  Clusters({this.clusterId, this.clusterHeadline, this.clusterSummary});

  Clusters.fromJson(Map<String, dynamic> json) {
    clusterId = json['cluster_id'];
    clusterHeadline = json['cluster_headline'];
    clusterSummary = json['cluster_summary'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['cluster_id'] = this.clusterId;
    data['cluster_headline'] = this.clusterHeadline;
    data['cluster_summary'] = this.clusterSummary;
    return data;
  }
}

class Recommends {
  String recommendId;
  String userId;
  String clusterId;

  Recommends({this.recommendId, this.userId, this.clusterId});

  Recommends.fromJson(Map<String, dynamic> json) {
    recommendId = json['recommend_id'];
    userId = json['user_id'];
    clusterId = json['cluster_id'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['recommend_id'] = this.recommendId;
    data['user_id'] = this.userId;
    data['cluster_id'] = this.clusterId;
    return data;
  }
}

class ApiUser {
  String userId;

  ApiUser({this.userId});

  ApiUser.fromJson(Map<String, dynamic> json) {
    userId = json['user_id'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['user_id'] = this.userId;
    return data;
  }
}

class Bookmarks {
  String favoriteId;
  String userId;
  String newsSummary;

  Bookmarks({this.favoriteId, this.userId, this.newsSummary});

  Bookmarks.fromJson(Map<String, dynamic> json) {
    favoriteId = json['favorite_id'];
    userId = json['user_id'];
    newsSummary = json['news_summary'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['favorite_id'] = this.favoriteId;
    data['user_id'] = this.userId;
    data['news_summary'] = this.newsSummary;
    return data;
  }
}

class Rating {
  String ratingId;
  int score;
  String userId;
  String newsSummary;

  Rating({this.ratingId, this.score, this.userId, this.newsSummary});

  Rating.fromJson(Map<String, dynamic> json) {
    ratingId = json['rating_id'];
    score = json['score'];
    userId = json['user_id'];
    newsSummary = json['news_summary'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['rating_id'] = this.ratingId;
    data['score'] = this.score;
    data['user_id'] = this.userId;
    data['news_summary'] = this.newsSummary;
    return data;
  }
}

class AllUserBookmarks {
  String headline;
  String summary;

  AllUserBookmarks({this.headline, this.summary});

  AllUserBookmarks.fromJson(Map<String, dynamic> json) {
    headline = json['headline'];
    summary = json['summary'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['headline'] = this.headline;
    data['summary'] = this.summary;
    return data;
  }
}