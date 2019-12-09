import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/services/auth_service.dart';

class ApiService {
  static final initialurl = "http://34.84.147.192:8000/news/";
  static final defaultClusterId = '07f269a8-3ae6-4994-abfd-e2cb2d4633f3';

  static Future<List<Clusters>> getRecommends() async {
    List<Recommends> recommends = List();
    FirebaseUser user = await AuthService.getCurrentUser();
    final response = await http.get(
      Uri.encodeFull(initialurl + "recommend/?format=json&user_id=" + user.uid), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      recommends = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Recommends.fromJson(data))
          .toList();
      if (recommends.length == 0){
        return null;
      }
      return getClustersByRecommends(recommends);
    } else {
      return null;
    }
  }

  static Future<List<Clusters>> getClustersByRecommends(recommendsList) async {
    List<Clusters> clusters = List();
    for (var i = 0; i < recommendsList.length; i++){
      final response = await http.get(
        Uri.encodeFull(initialurl + "clusters/?format=json&cluster_id=" + recommendsList[i].clusterId), 
        headers: {"Accept" : "application/json"}
      );
      if (response.statusCode == 200) {     
        List<Clusters> cluster = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Clusters.fromJson(data))
          .toList();
        clusters.add(cluster[0]);
      } 
    }
    return clusters;
  }

  static Future<ArticlePagination> getArticles(nextUrl) async {
    var url = initialurl + "articles/?format=json&limit=100";
    if (nextUrl != null) {
      url = nextUrl;
    }
    ArticlePagination articles;
    final response = await http.get(
      Uri.encodeFull(url), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {
      articles = ArticlePagination.fromJson(json.decode(utf8.decode(response.bodyBytes)));
      if (articles.results.length == 0){
        return null;
      }
      return articles;
    } else {
      return null;
    }
  }

  static Future<ArticlePagination> getArticlesByClusterId(clusterId) async {
    var url = initialurl + "articles/?cluster_id=" + clusterId + "&format=json&limit=10";
    ArticlePagination articles;
    final response = await http.get(
      Uri.encodeFull(url), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {
      articles = ArticlePagination.fromJson(json.decode(utf8.decode(response.bodyBytes)));
      if (articles.results.length == 0){
        return null;
      }
      return articles;
    } else {
      return null;
    }
  }

  static Future<ArticlePagination> getArticlesByCategory(category) async {
    ArticlePagination articles;
    final response = await http.get(
      Uri.encodeFull(initialurl + "articles/?format=json&limit=100&category=" + category), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {
      articles = ArticlePagination.fromJson(json.decode(utf8.decode(response.bodyBytes)));
      if (articles.results.length == 0){
        return null;
      }
      return articles;
    } else {
      return null;
    }
  }

  static Future getAllClusters() async {
    List<Clusters> clusters = List();
    final response = await http.get(
      Uri.encodeFull(initialurl + "clusters/?format=json&ordering=cluster_size"), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      clusters = (json.decode(utf8.decode(response.bodyBytes)) as List)
        .map((data) => new Clusters.fromJson(data))
        .toList();
      if (clusters.length <= 1){
        return null;
      }
      return removeDefaultCluster(clusters);
    } else {
      return null;
    }
  }

  static Future getAllClustersByCategory(category) async {
    List<Clusters> clusters = List();
    final response = await http.get(
      Uri.encodeFull(initialurl + "clusters/?format=json&ordering=cluster_size&cluster_category=" + category), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      clusters = (json.decode(utf8.decode(response.bodyBytes)) as List)
        .map((data) => new Clusters.fromJson(data))
        .toList();
      if (clusters.length <= 1){
        return null;
      }
      return clusters;
    } else {
      return null;
    }
  }

  static List<Clusters> removeDefaultCluster(clusters){
    var index;
    for (var i = 0; i < clusters.length; i++){
      if (clusters[i].clusterId == defaultClusterId){
        index = i;
      }
    }
    if (index != null){
      clusters.removeAt(index);
      return clusters;
    }
    return clusters;
  }

  static Future creatUser(uid) async {
    var jsonData = {"user_id" : uid};
    final response = await http.post(
      Uri.encodeFull(initialurl + "users/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 201){
      print("User Create Success!");
    }
  }

  static Future<List<UserRating>> getUserRating() async {
    List<UserRating> userRating = List();
    FirebaseUser user = await AuthService.getCurrentUser();
    final response = await http.get(
      Uri.encodeFull(initialurl + "rating/?format=json&user_id=" + user.uid), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      userRating = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new UserRating.fromJson(data))
          .toList();
      if (userRating.length == 0){
        return null;
      }
      return userRating;
    } else {
      return null;
    }
  }

  static Future creatRating(score, newsId) async {
    FirebaseUser user = await AuthService.getCurrentUser();
    var jsonData = {
        "score": score,
        "user_id": user.uid,
        "news_summary": newsId,
    };
    final response = await http.post(
      Uri.encodeFull(initialurl + "rating/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 201){
      return true;
    }
    return false;
  }

  static Future updateRating(score, newsId, ratingId) async {
    FirebaseUser user = await AuthService.getCurrentUser();
    var jsonData = {
        "score": score,
        "user_id": user.uid,
        "news_summary": newsId,
    };
    final response = await http.put(
      Uri.encodeFull(initialurl + "rating/" + ratingId + "/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200){
      return true;
    }
    return false;
  }

  static Future<List<AllUserBookmarks>> getBookmarksByUser() async {
    List<Bookmarks> bookmarks = List();
    FirebaseUser user = await AuthService.getCurrentUser();
    final response = await http.get(
      Uri.encodeFull(initialurl + "bookmarks/?format=json&user_id=" + user.uid), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      bookmarks = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Bookmarks.fromJson(data))
          .toList();
      if (bookmarks.length == 0){
        return null;
      }
      return getBookmarks(bookmarks);
    } else {
      return null;
    }
  }

  static Future<List<AllUserBookmarks>> getBookmarks(bookmarks) async {
    List<AllUserBookmarks> allUserBookmarks = List();
    for (var i = 0; i < bookmarks.length; i++){
      final response = await http.get(
        Uri.encodeFull(initialurl + "allbookmarks/?format=json&allUserFavorite_id=" + bookmarks[i].allUserFavId), 
        headers: {"Accept" : "application/json"}
      );
      if (response.statusCode == 200) {     
        List<AllUserBookmarks> allUserBookmark = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new AllUserBookmarks.fromJson(data))
          .toList();
        allUserBookmarks.add(allUserBookmark[0]);
      } 
    }
    return allUserBookmarks;
  }

  static Future creatBookmark(newsId, headline, summary) async {
    AllUserBookmarks bookmark;
    var jsonData = {
        "headline": headline,
        "summary": summary,
        "news_id": newsId,
    };
    final response = await http.post(
      Uri.encodeFull(initialurl + "allbookmarks/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 201){
      bookmark = AllUserBookmarks.fromJson(json.decode(utf8.decode(response.bodyBytes)));
      FirebaseUser user = await AuthService.getCurrentUser();
      jsonData = {
        "user_id": user.uid,
        "allUserFav_id": bookmark.allUserFavoriteId,
      };
      final responseTwo = await http.post(
        Uri.encodeFull(initialurl + "bookmarks/"), 
        body: jsonData,
        headers: {"Accept" : "application/json"}
      );
      if (responseTwo.statusCode == 201){
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  }

  static Future delBookmark(bookmarkId) async {
    final response = await http.delete(Uri.encodeFull(initialurl + "allbookmarks/" + bookmarkId + "/"));
    if (response.statusCode == 204){
      return true;
    }
    return false;
  }

}