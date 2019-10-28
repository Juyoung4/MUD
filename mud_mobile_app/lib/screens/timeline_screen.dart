import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class TimelineScreen extends StatefulWidget {
  @override
  _TimelineScreenState createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {

  final String url = 'https://newsapi.org/v2/top-headlines?country=kr&apiKey=e12b2ee6e72c4abbb34d3462f8f00120';
  List articles;
  bool isSwitched = false;

  Future<String> getData() async {
    var res = await http.get(Uri.encodeFull(url), headers: {"Accept" : "application/json"});
    setState(() {
      var resbody = json.decode(res.body);
      articles = resbody["articles"];
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
      body: AnnotatedRegion<SystemUiOverlayStyle>(
        value: SystemUiOverlayStyle.dark,
        child: CustomScrollView(
          primary: true,
          slivers: <Widget>[
            SliverAppBar(
              expandedHeight: 80.0,
              elevation: 0.0,
              floating: false,
              pinned: true,
              backgroundColor: Color(0xFFFAFAFA),
              flexibleSpace: FlexibleSpaceBar(
                centerTitle: false,
                titlePadding: EdgeInsets.only(left: 16.0, bottom: 8.0),
                title: Text('News App', style: myTextStyleDark),
              ),
            ),
            SliverFillRemaining(
              child: articles == null ? Container(child: Center(child: SpinKitRing(color: Colors.blueAccent),),) : ListView.builder(
                itemCount: articles == null ? 0 : articles.length,
                itemBuilder: (BuildContext context, int index){
                  return Container(
                    child: Text(articles[index]["title"]),
                  );
                },
              ),
            )
          ],
        ),
      ),
    );
  }
}