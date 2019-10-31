import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class TimelineScreen extends StatefulWidget {
  @override
  _TimelineScreenState createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {

  final String url = 'http://34.84.147.192:8000/news/articles/?format=json';
  List articles;
  bool isSwitched = false;

  Future<String> getData() async {
    var res = await http.get(Uri.encodeFull(url), headers: {"Accept" : "application/json"});
    setState(() {
      var resbody = json.decode(utf8.decode(res.bodyBytes));
      articles = resbody;
    });
    return 'Success!';
  }

  @override
  void initState(){
    super.initState();
    this.getData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        primary: true,
        slivers: <Widget>[
          SliverAppBar(
            brightness: Brightness.light,
            expandedHeight: 80.0,
            elevation: 0.0,
            floating: false,
            pinned: true,
            backgroundColor: Color(0xFFFAFAFA),
            flexibleSpace: FlexibleSpaceBar(
              centerTitle: false,
              titlePadding: EdgeInsets.only(left: 16.0, bottom: 8.0),
              title: Text(
                'Today\'s News',
                style: TextStyle(
                  color: Color(0xFF398AE5),
                  fontFamily: 'OpenSans',
                  fontSize: 30.0,
                  fontWeight: FontWeight.bold,
                  shadows: <Shadow>[
                    Shadow(
                      offset: Offset.zero,
                      blurRadius: 5.0,
                      color: Colors.black45
                    ),
                  ], 
                )
              ),
            ),
          ),
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index){
                return Container(
                  padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                  child: articles == null ? Container(child: Center(child: LinearProgressIndicator(),),) : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Text(
                          articles[index]["articles_title"] == null ? 'Title' : articles[index]["articles_title"],
                          style: TextStyle(
                            color: Colors.black,
                            fontSize: 18.0,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Text(
                          articles[index]["articles_description"] == null ? 'Description' : articles[index]["articles_description"],
                          style: TextStyle(
                            color: Colors.black87,
                            fontSize: 16.0,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Text(
                          articles[index]["articles_author"] == null ? 'Author' : articles[index]["articles_author"],
                          style: TextStyle(
                            color: Colors.black54,
                            fontSize: 14.0,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
                      ),
                      Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(30),
                          color: Colors.black12
                        ),
                        height: 3.0,
                      )
                    ],
                  ),
                );
              },
              childCount: articles == null ? 1 : articles.length
            )
          ),
        ],
      ),
    );
  }
}