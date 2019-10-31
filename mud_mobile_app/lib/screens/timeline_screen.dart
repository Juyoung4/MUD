import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';

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
    final double devHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: Colors.white,
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Container(
              padding: EdgeInsets.only(bottom: 10.0),
              height: (devHeight / 2) * 0.4,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: <Widget>[
                  Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        child: FadeIn(1.0, Text("Today's News", style: kTopBarTitleStyle)),
                      ),
                      Container(
                        child: FadeIn(1.3, Text("Timeline", style: kTopBarTitleStyle)),
                      ),
                    ],
                  ),
                  FadeIn(1.6, Container(
                    height: (devHeight / 2) * 0.2,
                    child: Image.asset('assets/images/news.png'),
                    decoration: BoxDecoration(
                      boxShadow: [
                        BoxShadow(
                          color: Colors.greenAccent.withOpacity(0.3),
                          blurRadius: 20.0,
                          spreadRadius: 5.0,
                          offset: Offset(5.0, 5.0)
                        )
                      ]
                    ),
                  ))
                ],
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: articles == null ? 1 : articles.length,
                itemBuilder: (BuildContext contex, int index){
                  return Container(
                    padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                    child: articles == null ? Container(child: Center(child: CircularProgressIndicator(),),) : Column(
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
              ),
            )
          ],
        )
      ),
    );
  }
}