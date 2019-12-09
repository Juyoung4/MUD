import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:marquee/marquee.dart';
import 'package:mud_mobile_app/models/api_models.dart';
import 'api_service.dart';

class TtsService extends StatefulWidget {
  @override
  _TtsServiceState createState() => _TtsServiceState();
}
enum TtsState { playing, stopped }
class _TtsServiceState extends State<TtsService> {
  List<Clusters> clusters;
  FlutterTts flutterTts = FlutterTts();
  
  TtsState ttsState = TtsState.stopped;

  get isPlaying => ttsState == TtsState.playing;

  get isStopped => ttsState == TtsState.stopped;

  Future getData() async {
    List<Clusters> response = await ApiService.getAllClusters();
    if (response != null){
      if (this.mounted){
        setState(() {
          clusters = response;
        });
      }
    }
  }

  Future _speak(speek) async{
    await flutterTts.setLanguage("ko-KR");
    await flutterTts.setPitch(0.6);
    var result = await flutterTts.speak(speek);
    if (result == 1) setState(() => ttsState = TtsState.playing);
  }

  Future _stop() async{
      var result = await flutterTts.stop();
      if (result == 1) setState(() => ttsState = TtsState.stopped);
  }

  initTts() {
    flutterTts = FlutterTts();

    flutterTts.setStartHandler(() {
      setState(() {
        ttsState = TtsState.playing;
      });
    });

    flutterTts.setCompletionHandler(() {
      setState(() {
        print("Complete");
        ttsState = TtsState.stopped;
      });
    });

    flutterTts.setErrorHandler((msg) {
      setState(() {
        ttsState = TtsState.stopped;
      });
    });
  }

  @override
  void initState() { 
    super.initState();
    this.getData();
    initTts();
  }
 
  @override
  Widget build(BuildContext context) {
    final double devWidth = MediaQuery.of(context).size.width;
    return Container(
      height: 50.0,
      width: devWidth,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          GestureDetector(
            onTap: clusters == null ? (){} : (){
              if (isStopped){
                _speak(clusters[0].clusterSummary);
              } else {
                _stop();
              }
            },
            child: Container(
              child: isPlaying ? Image.asset('assets/images/pause.png') : Image.asset('assets/images/play.png')
            ),
          ),
          Container(
            alignment: Alignment.centerLeft,
            width: devWidth * 0.75,
            child: clusters == null ? Text(
              'Loading....',
              style: TextStyle(
                color: Colors.black,
                fontSize: 22,
                fontWeight: FontWeight.bold
              ),
            ) : Marquee(
              text: clusters[0].clusterSummary,
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 22),
              blankSpace: 20.0,
              pauseAfterRound: Duration(seconds: 1),
              startPadding: 10.0,
            ),
          ),
        ],
      ),
    );
  }
}