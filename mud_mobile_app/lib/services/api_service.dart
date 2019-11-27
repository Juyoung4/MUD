import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/services/auth_service.dart';

class ApiService {

  static Future<List<Clusters>> getRecommends() async {
    List<Recommends> recommends = List();
    FirebaseUser user = await AuthService.getCurrentUser();
    final response = await http.get(
      Uri.encodeFull("http://34.84.147.192:8000/news/recommend/?format=json&user_id=" + user.uid), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      recommends = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Recommends.fromJson(data))
          .toList();
      if (recommends.length == 0){
        return null;
      }
      return getClusters(recommends);
    } else {
      return null;
    }
  }

  static Future<List<Clusters>> getClusters(recommendsList) async {
    List<Clusters> clusters = List();
    for (var i = 0; i < recommendsList.length; i++){
      final response = await http.get(
        Uri.encodeFull("http://34.84.147.192:8000/news/clusters/?format=json&cluster_id=" + recommendsList[i].clusterId), 
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

  static Future<List<Article>> getArticlesByCategory(category) async {
    List<Article> articles = List();
    final response = await http.get(
      Uri.encodeFull("http://34.84.147.192:8000/news/articles/?format=json&category=" + category), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {
      articles = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Article.fromJson(data))
          .toList();
      if (articles.length == 0){
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
      Uri.encodeFull("http://34.84.147.192:8000/news/clusters/?format=json"), 
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 200) {     
      clusters = (json.decode(utf8.decode(response.bodyBytes)) as List)
        .map((data) => new Clusters.fromJson(data))
        .toList();
    } else {
      Clusters error = Clusters();
      error.clusterId = "Status Code : " + response.statusCode.toString();
      error.clusterHeadline = "Error Loading Data";
      error.clusterSummary = "News may have deleted from database";
      clusters.add(error);
    }
    return clusters;
  }

  static Future creatUser(uid) async {
    var jsonData = {"user_id" : uid};
    final response = await http.post(
      Uri.encodeFull("http://34.84.147.192:8000/news/users/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 201){
      print("User Create Success!");
    }
  }

  static Future creatBookmark(uid, headline, summary) async {
    AllUserBookmarks bookmark = AllUserBookmarks();
    var jsonData = {
      "headline": headline,
      "summary": summary,
    };
    final response = await http.post(
      Uri.encodeFull("http://34.84.147.192:8000/news/allbookmarks/"), 
      body: jsonData,
      headers: {"Accept" : "application/json"}
    );
    if (response.statusCode == 201){
      bookmark = AllUserBookmarks.fromJson(json.decode(utf8.decode(response.bodyBytes)));
    }
  }

}