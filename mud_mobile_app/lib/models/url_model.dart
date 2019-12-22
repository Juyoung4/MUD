import 'package:cloud_firestore/cloud_firestore.dart';

class Url {
  final String url;

  Url({this.url});

  factory Url.fromDoc(DocumentSnapshot doc) {
    return Url(
      url: doc['url'],
    );
  }
}