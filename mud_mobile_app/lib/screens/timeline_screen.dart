import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:mud_mobile_app/utilities/constants.dart';

class TimelineScreen extends StatefulWidget {
  @override
  _TimelineScreenState createState() => _TimelineScreenState();
}

class _TimelineScreenState extends State<TimelineScreen> {
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
          ],
        ),
      ),
    );
  }
}