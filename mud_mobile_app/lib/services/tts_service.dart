import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:marquee/marquee.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'api_service.dart';

class TtsService extends StatefulWidget {
  @override
  _TtsServiceState createState() => _TtsServiceState();
}

class _TtsServiceState extends State<TtsService> {
  List<Clusters> clusters;
  FlutterTts flutterTts = new FlutterTts();

  Future getData() async {
    List<Clusters> response = await ApiService.getAllClusters();
    setState(() {
      clusters = response;
    });
  }

  Future _speak(speek) async{
    await flutterTts.setLanguage("ko-KR");
    await flutterTts.setPitch(0.8);
    await flutterTts.speak(speek);
  }

  @override
  void initState() { 
    super.initState();
    this.getData();
  }
 
  @override
  Widget build(BuildContext context) {
    final double devWidth = MediaQuery.of(context).size.width;
    return Container(
      height: 100,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Container(
            child: IconButton(
              icon: Icon(
                Icons.speaker_phone,
                size: 48,
                color: Colors.green,
              ),
              onPressed: clusters == null ? (){} : (){
                print(clusters[1].clusterHeadline);
                _speak(clusters[1].clusterHeadline);
              },
            ),
            decoration: BoxDecoration(
              boxShadow: [
                BoxShadow(
                  color: Colors.greenAccent.withOpacity(0.1),
                  blurRadius: 20.0,
                  spreadRadius: 5.0,
                  offset: Offset(5.0, 5.0)
                )
              ]
            ),
          ),
          Container(
            width: (devWidth / 4) * 3,
            child: clusters == null ? Text(
              'Loading....',
              style: TextStyle(
                color: Colors.black,
                fontSize: 24,
                fontWeight: FontWeight.bold
              ),
            ) : Marquee(
              text: clusters[1].clusterHeadline,
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 26),
              blankSpace: 20.0,
              pauseAfterRound: Duration(seconds: 1),
              startPadding: 10.0,
            ),
          )
        ],
      ),
    );
  }
}