import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'package:mud_mobile_app/services/api_service.dart';
import 'package:mud_mobile_app/services/tts_service.dart';
import 'package:mud_mobile_app/utilities/constants.dart';
import 'dart:async';
import 'package:mud_mobile_app/utilities/fade_in_animation.dart';

class TimelineScreen extends StatefulWidget {
  @override
  _TimelineScreenState createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {
  List<Article> articles;
  List<Clusters> clusters;
  bool isSwitched = false;

  Future getData() async {
    List<Clusters> response = await ApiService.getRecommends();
    setState(() {
      clusters = response;
    });
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
                        child: FadeIn(1.2, Text("Timeline", style: kTopBarTitleStyle)),
                      ),
                    ],
                  ),
                  FadeIn(1.4, Container(
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
            FadeIn(1.6, TtsService()),
            Flexible(
              child: FadeIn(1.6, ListView.builder(
                  itemCount: clusters == null ? 1 : clusters.length,
                  itemBuilder: (BuildContext contex, int index){
                    return Container(
                      padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                      child: clusters == null ? Container(child: Center(child: CircularProgressIndicator(),),) : Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Text(
                              clusters[index].clusterHeadline == null ? 'Headline' : clusters[index].clusterHeadline,
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
                              clusters[index].clusterSummary == null ? 'Summary' : clusters[index].clusterSummary,
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
                              clusters[index].clusterId == null ? 'ID' : clusters[index].clusterId,
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
              ),
            )
          ],
        )
      ),
    );
  }
}