import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/services/auth_service.dart';

class ApiService {
  static List<Article> articles = List();
  static List<Clusters> clusters = List();
  static List<Recommends> recommends = List();

  static Future getArticles() async {
    final response = await http.get(Uri.encodeFull("http://34.84.147.192:8000/news/articles/?format=json"), headers: {"Accept" : "application/json"});
    if (response.statusCode == 200) {
      articles = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Article.fromJson(data))
          .toList();
      return articles;
    } else {
      return null;
    }
  }

  static Future getRecommends() async {
    FirebaseUser user = await AuthService.getCurrentUser();
    final response = await http.get(Uri.encodeFull("http://34.84.147.192:8000/news/recommend/?format=json&user_id=" + user.uid), headers: {"Accept" : "application/json"});
    if (response.statusCode == 200) {     
      recommends = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Recommends.fromJson(data))
          .toList();
      return getClusters(recommends);
    } else {
      Clusters error = Clusters();
      error.clusterId = "Status Code : " + response.statusCode.toString();
      error.clusterHeadline = "Error Loading Data";
      error.clusterSummary = "User may not have Recommending Profile";
      print(error.clusterHeadline);
      clusters.add(error);
      return clusters;
    }
  }

  static Future getClusters(recommendsList) async {
    for (var i = 0; i < recommendsList.length; i++){
      final response = await http.get(Uri.encodeFull("http://34.84.147.192:8000/news/clusters/?format=json&cluster_id=" + recommendsList[i].clusterId), headers: {"Accept" : "application/json"});
      if (response.statusCode == 200) {     
        List<Clusters> cluster = (json.decode(utf8.decode(response.bodyBytes)) as List)
          .map((data) => new Clusters.fromJson(data))
          .toList();
        clusters.add(cluster[0]);
      } else {
        Clusters error = Clusters();
        error.clusterId = "Status Code : " + response.statusCode.toString();
        error.clusterHeadline = "Error Loading Data";
        error.clusterSummary = "News may have deleted from database";
        clusters.add(error);
      }
    }
    return clusters;
  }
}