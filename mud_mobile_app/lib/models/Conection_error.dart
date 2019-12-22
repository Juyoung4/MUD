import 'package:flutter/material.dart';

class ErrorDisplay extends StatefulWidget {
  final String errorDisplay;
  final bool error;
  ErrorDisplay({this.errorDisplay, this.error});
  @override
  _ErrorDisplayState createState() => _ErrorDisplayState();
}

class _ErrorDisplayState extends State<ErrorDisplay> {
  @override
  Widget build(BuildContext context) {
    final double devWidth = MediaQuery.of(context).size.width;
    return Center(
      child: Column(
        children: <Widget>[
          widget.error ? Image(
            image: AssetImage('assets/images/error.png'),
            height: devWidth,
            fit: BoxFit.fitHeight,
          ) : Container(
            height: 10,
          ),
          Container(
            padding: EdgeInsets.all(20),
            child: Text(widget.errorDisplay, style: TextStyle(color: Colors.deepOrangeAccent, fontSize: 26.0, fontWeight: FontWeight.bold),),
          )
        ],
      ),
    );
  }
}